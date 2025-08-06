from fastapi import HTTPException


class RBShop:
    def __init__(
            self,
            street_id: int | None = None,
            street_name: str | None = None,
            city_id: int | None = None,
            city_name: str | None = None,
            is_open: int | None = None,
    ):
        self.street_id = street_id
        self.street_name = street_name
        self.city_id = city_id
        self.city_name = city_name

        if is_open is not None:
            if is_open < 0 or is_open > 1:
                raise HTTPException(detail="Параметр is_open может принимать только 1 или 0", status_code=400)

        self.is_open = is_open


    def to_dict(self):
        filtered_data = {
            "street_id": self.street_id,
            "street_name": self.street_name,
            "city_id": self.city_id,
            "city_name": self.city_name,
            "is_open": self.is_open,
        }
        return filtered_data