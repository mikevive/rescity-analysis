from application.bounded_contexts.analysis.domain.model.kpi_group import KpiGroup
from src.application.services.dtos.kpi_group_created_dto import KpiGroupCreatedDto

class KpiGroupCreatedMapper:

  @staticmethod
  def to_dto(kpi_group: KpiGroup) -> KpiGroupCreatedDto:
    return KpiGroupCreatedDto(
      str(kpi_group.get_id())
    )