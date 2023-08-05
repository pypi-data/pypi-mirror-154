import requests


class MLFlowAPI:
    """API to interact with MLFlow"""

    def __init__(self, mlflowRoot):
        self.mlflowRoot = mlflowRoot

    def getExperiment(self, experiment_id):
        """
        Get the experiment with the given id

        :param id: experiment id
        :return: experiment
        """
        url = f"{self.mlflowRoot}/2.0/mlflow/experiments/get"
        r = requests.get(url, json={"experiment_id": experiment_id})
        result_dict = r.json()
        return result_dict["experiment"]

    def getExperiments(self):
        """Get all the experiments"""
        url = f"{self.mlflowRoot}/2.0/mlflow/experiments/list"
        r = requests.get(url)
        result_dict = r.json()
        return result_dict["experiments"]

    def getExperimentRuns(
        self,
        experiment_id,
        filter_string=None,
        max_results=50000,
        order_by=None,
        page_token=None,
    ):
        """Get the runs with the given experiment id and other filters"""
        url = f"{self.mlflowRoot}/2.0/mlflow/runs/search"
        r = requests.post(
            url,
            json={
                "experiment_ids": [experiment_id],
                "filter_string": filter_string,
                "max_results": max_results,
                "order_by": order_by,
                "page_token": page_token,
            },
        )
        result_dict = r.json()
        return result_dict["runs"] if('runs' in result_dict) else []

    def getRunMetric(self, run_id, metric_key):
        """
        Get the experiment with the given id

        :param id: experiment id
        :return: experiment
        """
        url = f"{self.mlflowRoot}/2.0/mlflow/metrics/get-history"
        r = requests.get(url, json={"run_id": run_id, "metric_key": metric_key})
        result_dict = r.json()
        return result_dict["metrics"] if('metrics' in result_dict) else []


if __name__ == "__main__":
    mlflowRoot = "http://127.0.0.1:5000/api"
    mlflowAPI = MLFlowAPI(mlflowRoot)
    experiments = mlflowAPI.getExperiments()
    experiments = [
        mlflowAPI.getExperiment(experiment["experiment_id"])
        for experiment in experiments
    ]
    print(experiments)
    runs = mlflowAPI.getExperimentRuns(experiment_id=experiments[1]["experiment_id"])
    print(runs)
