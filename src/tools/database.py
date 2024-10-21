from sqlalchemy import select


async def get_object(model, fileter_by, session):
    query = select(model).where(fileter_by)
    result = await session.execute(query)
    obj = result.scalar_one_or_none()
    return obj


def update_model_instance(instance, data):
    for key, value in data.items():
        setattr(instance, key, value)