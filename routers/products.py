from fastapi import APIRouter, status

router = APIRouter(
    prefix='/products',
    tags=['products']
)

@router.get('/')
async def get_all_products():
    return {'message': 'Отслеживаемые товары'}

@router.get('/{product_id}')
async def get_product(product_id: int):
    return {'product_id': product_id}

@router.post('/{product_id}')
async def add_product(product_id: int):
    return {'product_id': product_id}

@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    pass