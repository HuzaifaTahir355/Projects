from uuid import uuid4

class UniqueIdGenerator:
    def get_unique_id(length_of_ids: int):
        if length_of_ids > 1:
            return [str(uuid4()) for _ in range(length_of_ids)]
        else:
            return str(uuid4())