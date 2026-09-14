"""
Сервисный слой для взаимодействия с моделями машинного обучения.
Обертка над CatBoost и PyTorch Transformer.
"""

import json
import os
from typing import Any

import pandas as pd
import torch
from app.schemas.requests import UserProfile
from catboost import CatBoostClassifier, CatBoostRegressor, Pool
from torch import nn

LEVEL_MAP = {"Novice": 0, "Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}

INVENTORY_MAP = {
    "Medicine Ball": "Machine",
    "Cable": "Machine",
    "Machine": "Machine",
    "Kettlebell": "Dumbbell",
    "Dumbbell": "Dumbbell",
    "Barbell": "Barbell",
    "Band": "Bodyweight",
    "Body Only": "Bodyweight",
    "Other": "Machine",
    "Foam Roll": "Bodyweight",
    "Bands": "Bodyweight",
    "Cardio": "Bodyweight",
    "Bodyweight": "Bodyweight",
}


class TransformerRec(nn.Module):
    """
    BERT-подобный энкодер для задачи секвенциальных рекомендаций.
    """

    def __init__(
        self,
        vocab_size: int,
        hidden: int = 256,
        heads: int = 8,
        layers: int = 4,
        max_len: int = 20,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        self.token_emb = nn.Embedding(vocab_size, hidden)
        self.pos_emb = nn.Embedding(max_len, hidden)
        self.dropout = nn.Dropout(dropout)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden, nhead=heads, dropout=dropout, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=layers)
        self.fc = nn.Linear(hidden, vocab_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Прямой проход трансформера."""
        positions = torch.arange(x.size(1), device=x.device).unsqueeze(0)
        x = self.dropout(self.token_emb(x) + self.pos_emb(positions))
        x = self.transformer(x)
        return self.fc(x)


class MLService:
    """
    Основной класс-обертка для всех задач предсказания (рекомендации + регрессия).
    """

    def __init__(self) -> None:
        self.device = torch.device("cpu")
        self.assets_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "models")
        )

        with open(
            os.path.join(self.assets_dir, "encoder", "vocab.json"),
            "r",
            encoding="utf-8",
        ) as f:
            self.vocab = json.load(f)
        self.id2name = {int(v): k for k, v in self.vocab.items()}

        self.exercise_meta_dict: dict[str, dict[str, Any]] = {}

        try:
            df_equip = pd.read_csv(
                os.path.join(
                    self.assets_dir, "metadata", "id_to_equipment_mapping_FIXED.csv"
                )
            )
            self.id_to_eq_dict = df_equip.set_index("candidate_id")[
                "equipment_golden"
            ].to_dict()
        except FileNotFoundError:
            self.id_to_eq_dict = {}

        self.transformer = TransformerRec(vocab_size=len(self.vocab)).to(self.device)
        bert_path = os.path.join(
            self.assets_dir, "encoder", "gym_bert_v2_ep27_hit0.3522.pth"
        )
        if os.path.exists(bert_path):
            self.transformer.load_state_dict(
                torch.load(bert_path, map_location=self.device)
            )
            self.transformer.eval()
            print("Loaded Transformer Model")

        self.cat_ranker = CatBoostClassifier()
        cat_path = os.path.join(
            self.assets_dir, "ranker", "catboost_recommender_final.cbm"
        )
        if os.path.exists(cat_path):
            self.cat_ranker.load_model(cat_path)
            print("Loaded CatBoost Ranker")

        self.regressor_light = CatBoostRegressor()
        light_path = os.path.join(
            self.assets_dir, "regressor", "weight_predictor_light.cbm"
        )
        if os.path.exists(light_path):
            self.regressor_light.load_model(light_path)
            print("Loaded Regressor LIGHT")

        self.regressor_pro = CatBoostRegressor()
        pro_path = os.path.join(
            self.assets_dir, "regressor", "weight_predictor_pro.cbm"
        )
        if os.path.exists(pro_path):
            self.regressor_pro.load_model(pro_path)
            print("Loaded Regressor PRO")

    def recommend(
        self, history_ids: list[int], profile: UserProfile, top_k: int = 10
    ) -> list[dict[str, Any]]:
        """
        Двухэтапный конвейер рекомендаций (Трансформер + CatBoost).
        """
        if not history_ids:
            return []

        input_seq = torch.LongTensor([history_ids]).to(self.device)
        with torch.no_grad():
            logits = self.transformer(input_seq)
            probs = torch.softmax(logits[0, -1, :], dim=-1)

        scores, indices = torch.topk(probs, k=100)
        candidates = []

        last_ex_name = self.id2name.get(history_ids[-1], "")
        last_meta = self.exercise_meta_dict.get(last_ex_name, {})

        for s, idx in zip(scores.cpu().numpy(), indices.cpu().numpy()):
            idx_val = int(idx)
            name = self.id2name.get(idx_val, "Unknown")
            current_meta = self.exercise_meta_dict.get(name, {})
            is_same = (
                1
                if current_meta.get("category") == last_meta.get("category")
                and last_meta
                else 0
            )

            raw_eq = self.id_to_eq_dict.get(idx_val, "Unknown")
            mapped_eq = INVENTORY_MAP.get(raw_eq, raw_eq)

            candidates.append(
                {
                    "bert_score": float(s),
                    "candidate_id": str(idx_val),
                    "is_same_group": is_same,
                    "eq_clean": str(mapped_eq),
                    "level_idx": LEVEL_MAP.get(profile.level, 1),
                    "goal_clean": str(profile.goal),
                    "raw_equipment": raw_eq,
                    "name": name,
                }
            )

        cand_df = pd.DataFrame(candidates)
        features_order = [
            "bert_score",
            "candidate_id",
            "is_same_group",
            "eq_clean",
            "level_idx",
            "goal_clean",
        ]

        preds = self.cat_ranker.predict_proba(cand_df[features_order])[:, 1]
        cand_df["final_score"] = preds

        if profile.equipment != "All (Gym Mixed)":
            cand_df = cand_df[cand_df["eq_clean"] == profile.equipment]

        final_df = cand_df.sort_values("final_score", ascending=False).head(top_k)

        results = []
        for _, row in final_df.iterrows():
            results.append(
                {
                    "exercise_name": row["name"],
                    "exercise_id": int(row["candidate_id"]),
                    "final_score": round(float(row["final_score"]), 2),
                    "bert_score": float(row["bert_score"]),
                    "equipment": row["raw_equipment"],
                }
            )

        return results

    def predict_weight(
        self, profile: UserProfile, exercise_name: str, base_lift: str, raw_eq: str
    ) -> tuple[float, int]:
        """
        Предсказывает целевой вес и количество повторений (Регрессор).
        """
        has_records = sum(profile.sbd) > 0 if profile.sbd else False
        exercise_id = str(self.vocab.get(exercise_name, 0))

        if has_records:
            cols = [
                "Sex",
                "Age",
                "BodyweightKg",
                "Best3SquatKg",
                "Best3BenchKg",
                "Best3DeadliftKg",
                "goal_clean",
                "level_idx",
                "Base_Lift",
                "eq_clean",
                "exercise_id",
            ]
            input_data = {
                "Sex": profile.sex,
                "Age": profile.age,
                "BodyweightKg": profile.bw,
                "Best3SquatKg": profile.sbd[0],
                "Best3BenchKg": profile.sbd[1],
                "Best3DeadliftKg": profile.sbd[2],
                "goal_clean": profile.goal,
                "level_idx": LEVEL_MAP.get(profile.level, 1),
                "Base_Lift": base_lift or "None",
                "eq_clean": INVENTORY_MAP.get(raw_eq, "Machine"),
                "exercise_id": exercise_id,
            }
            model = self.regressor_pro
            cat_features = ["Sex", "goal_clean", "Base_Lift", "eq_clean", "exercise_id"]
        else:
            cols = [
                "Sex",
                "Age",
                "BodyweightKg",
                "goal_clean",
                "level_idx",
                "eq_clean",
                "exercise_id",
            ]
            input_data = {
                "Sex": profile.sex,
                "Age": profile.age,
                "BodyweightKg": profile.bw,
                "goal_clean": profile.goal,
                "level_idx": LEVEL_MAP.get(profile.level, 1),
                "eq_clean": INVENTORY_MAP.get(raw_eq, "Machine"),
                "exercise_id": exercise_id,
            }
            model = self.regressor_light
            cat_features = ["Sex", "goal_clean", "eq_clean", "exercise_id"]

        input_df = pd.DataFrame([input_data])[cols]
        pred = model.predict(Pool(input_df, cat_features=cat_features))[0]

        weight, reps = round(float(pred[0]), 1), int(pred[1])
        eq_clean_val = INVENTORY_MAP.get(raw_eq, "Machine").lower()

        if "dumbbell" in eq_clean_val:
            weight = max(2.0, round(weight / 2) * 2)
        elif "machine" in eq_clean_val:
            weight = max(5.0, round(weight / 5) * 5)

        return weight, max(1, reps)


ml_service = MLService()
