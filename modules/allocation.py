from ortools.linear_solver import pywraplp
import asyncio
import logging

logger = logging.getLogger(__name__)

class HospitalResourceAllocator:
    """Allocates hospital resources based on patient triage."""

    def __init__(self, hospitals, patients):
        self.hospitals = hospitals
        self.patients = patients

    async def allocate_resources(self):
        """Optimize resource allocation using linear programming."""
        solver = pywraplp.Solver.CreateSolver('SCIP')
        hospital_names = list(self.hospitals.keys())
        patient_ids = [patient['id'] for patient in self.patients]

        # Decision variables
        x = {(i, j): solver.IntVar(0, 1, f'x_{i}_{j}') for i in patient_ids for j in hospital_names}

        # Constraints
        for i in patient_ids:
            solver.Add(sum(x[(i, j)] for j in hospital_names) == 1)

        for j in hospital_names:
            solver.Add(sum(x[(i, j)] for i in patient_ids) <= self.hospitals[j]['beds'])
            solver.Add(sum(x[(i, j)] for i in patient_ids if self.patients[i-1]['triage'] == 'Red') <= self.hospitals[j]['ambulances'])

        # Objective
        objective = solver.Objective()
        for i in patient_ids:
            for j in hospital_names:
                priority = 10 if self.patients[i-1]['triage'] == 'Red' else (5 if self.patients[i-1]['triage'] == 'Yellow' else 1)
                objective.SetCoefficient(x[(i, j)], priority)
        objective.SetMaximization()

        # Solve
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            logger.info("Optimal resource allocation found.")
            for i in patient_ids:
                for j in hospital_names:
                    if x[(i, j)].solution_value() == 1:
                        print(f"Patient {i} (Triage: {self.patients[i-1]['triage']}) -> {j}")
        else:
            logger.warning("No optimal solution found.")