from application.bounded_contexts.analysis.domain.model.kpi import Kpi
from application.services.dtos.kpi_created_dto import KpiCreatedDto

class KpiCreatedMapper:

  @staticmethod
  def to_dto(kpi: Kpi) -> KpiCreatedDto:
    return KpiCreatedDto(
      str(kpi.get_id())
    )