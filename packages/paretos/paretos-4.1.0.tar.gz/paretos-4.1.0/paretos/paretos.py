import asyncio
from typing import Dict, List, Optional, Union

from . import (
    AsyncEnvironmentInterface,
    EnvironmentInterface,
    OptimizationProblem,
    OptimizationResultInterface,
    TerminatorInterface,
)
from .config import Config
from .exceptions import OptimizationAlreadyStarted
from .service_locator import ServiceLocator


class Paretos:
    def __init__(self, config: Config):
        self.__service_locator = ServiceLocator(config=config)
        self.__is_optimization_started = False

    def optimize(
        self,
        name: str,
        optimization_problem: OptimizationProblem,
        environment: Union[EnvironmentInterface, AsyncEnvironmentInterface],
        terminators: Optional[List[TerminatorInterface]] = None,
        n_parallel: int = 1,
        resume: bool = False,
        use_case_id: Optional[str] = None,
        company_id: Optional[str] = None,
    ) -> None:
        process = self.optimize_async(
            name=name,
            optimization_problem=optimization_problem,
            environment=environment,
            terminators=terminators,
            n_parallel=n_parallel,
            resume=resume,
            use_case_id=use_case_id,
            company_id=company_id,
        )

        asyncio.run(process)

    async def optimize_async(
        self,
        name: str,
        optimization_problem: OptimizationProblem,
        environment: Union[EnvironmentInterface, AsyncEnvironmentInterface],
        terminators: Optional[List[TerminatorInterface]] = None,
        n_parallel: int = 1,
        resume: bool = False,
        use_case_id: Optional[str] = None,
        company_id: Optional[str] = None,
    ) -> None:
        if self.__is_optimization_started:
            # refactor: database transactional lock in the future
            raise OptimizationAlreadyStarted()

        self.__is_optimization_started = True

        optimize_handler = self.__service_locator.optimize_handler

        try:
            await optimize_handler.optimize_async(
                name=name,
                optimization_problem=optimization_problem,
                environment=environment,
                terminators=terminators,
                n_parallel=n_parallel,
                resume=resume,
                use_case_id=use_case_id,
                company_id=company_id,
            )
        finally:
            self.__is_optimization_started = False

    def obtain(self, name: str) -> OptimizationResultInterface:
        obtain_handler = self.__service_locator.obtain_handler

        return obtain_handler.obtain(name=name)

    def export(self, name: str) -> List[Dict]:
        export_handler = self.__service_locator.export_handler

        return export_handler.export(project_name=name)

    def predict(self, model: str, data: List[Dict[str, List[float]]]) -> dict:
        predict_handler = self.__service_locator.predict_handler

        return predict_handler.predict(model, data)

    def upload_training_data_file(self, use_case_id: str, file_path: str) -> None:
        use_case_handler = self.__service_locator.use_case_handler

        return use_case_handler.upload_training_data_file(use_case_id, file_path)
