from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from uuid import UUID
from typing import Any, Dict

from ...core.database import get_db
from ...models.sample import Sample, SampleStatus
from ...core.pubsub import broker

router = APIRouter(prefix="/samples", tags=["samples"])

@router.put("/{sample_id}/status", response_model=Dict[str, Any])
async def update_sample_status(
    sample_id: UUID = Path(..., title="The ID of the sample to update"),
    status: SampleStatus = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Updates the status of a specific sample.
    """
    if status is None:
        raise HTTPException(status_code=422, detail="Status is required")

    # Fetch the sample
    result = await db.execute(select(Sample).where(Sample.id == sample_id))
    sample = result.scalars().first()
    
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    # Update status
    sample.status = status
    await db.commit()
    await db.refresh(sample)

    await broker.publish("events", {
        "event": "SAMPLE_PROCESSED" if getattr(status, "value", status) == "processed" else "STATUS_CHANGED",
        "sample_id": str(sample.id),
        "status": getattr(status, "value", status)
    })

    return {
        "id": str(sample.id),
        "status": sample.status.value,
        "message": "Status updated successfully"
    }
