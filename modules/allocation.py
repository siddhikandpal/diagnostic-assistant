import pandas as pd
from ortools.linear_solver import pywraplp
import logging

logger = logging.getLogger(__name__)

class HospitalResourceAllocator:
    def __init__(self, hospitals, data_file):
        self.hospitals = hospitals
        self.patients = self.load_patients(data_file)

    def load_patients(self, data_file):
        """Load patients from CSV instead of hardcoded config.yaml patients"""
        df = pd.read_csv(data_file)
        patients = {
            f"Patient {i+1}": {
                "id": i+1,
                "triage": row["triage_category"]
            }
            for i, row in df.iterrows()
        }
        print("\n📌 Loaded Patients from CSV:", patients)  # Debugging output
        return patients

    def allocate_resources(self):
        solver = pywraplp.Solver.CreateSolver("SCIP")
        if not solver:
            logger.error("❌ SCIP solver could not be created.")
            return

        hospital_names = list(self.hospitals.keys())

        # 🔹 Sort patients: Prioritize Red > Yellow > Green
        triage_priority = {"Red": 3, "Yellow": 2, "Green": 1}
        sorted_patients = sorted(self.patients.items(), key=lambda p: triage_priority[p[1]["triage"]], reverse=True)
        patient_ids = {details["id"]: name for name, details in sorted_patients}

        # Decision variables
        x = {(i, j): solver.IntVar(0, 1, f"x_{i}_{j}") for i in patient_ids.keys() for j in hospital_names}

        # Constraints
        for i in patient_ids.keys():
            solver.Add(sum(x[(i, j)] for j in hospital_names) == 1)  # Ensure each patient is assigned to one hospital

        for j in hospital_names:
            solver.Add(sum(x[(i, j)] for i in patient_ids.keys()) <= self.hospitals[j]["capacity"])  # Capacity constraint

            if "ambulances" in self.hospitals[j]:  # Ensure Red patients get priority in hospitals with ambulances
                solver.Add(
                    sum(x[(i, j)] for i in patient_ids.keys() if self.patients[patient_ids[i]]["triage"] == "Red")
                    <= max(1, self.hospitals[j]["ambulances"])
                )

        # Objective: Prioritize Red > Yellow > Green
        objective = solver.Objective()
        for i in patient_ids.keys():
            for j in hospital_names:
                triage = self.patients[patient_ids[i]]["triage"]
                priority = 10 if triage == "Red" else (5 if triage == "Yellow" else 1)
                objective.SetCoefficient(x[(i, j)], priority)
        objective.SetMaximization()

        # Solve
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            logger.info("✅ Optimal resource allocation found.")
            print("\n🚑 **Final Patient-Hospital Allocation:**")
            for i in patient_ids.keys():
                allocated = False
                for j in hospital_names:
                    if x[(i, j)].solution_value() == 1:
                        print(f"✅ Patient {i} (Triage: {self.patients[patient_ids[i]]['triage']}) -> {j}")
                        allocated = True
                        break
                if not allocated:
                    print(f"❌ Patient {i} (Triage: {self.patients[patient_ids[i]]['triage']}) was NOT allocated to any hospital.")
        else:
            logger.warning("⚠️ No optimal solution found.")
            print("❌ No optimal solution found. Please check hospital capacities or constraints.")
