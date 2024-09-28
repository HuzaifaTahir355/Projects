from fastapi import APIRouter, status
from interactor import product_description_interactor
from schema import ProductDescriptionRequest

router = APIRouter(
    tags=["Product Description"]
)


@router.get('/get-available-llms', status_code=status.HTTP_200_OK)
def available_llms():
    return product_description_interactor.get_available_llms()


@router.post("/process-data", status_code=status.HTTP_200_OK)
def get_product_description(request: ProductDescriptionRequest):
    return product_description_interactor.generate_product_description(request.languages)
