"""Train script."""
import argparse
from fraud.data import repositories
from fraud import ml


def main(do_hpo: bool):
    """Execute main script.

    Args:
        do_hpo: If true, the hyperparameters will be optimized.

    Returns:
        model scores.
    """
    estimator = ml.EstimatorFactory().create(
        estimator_type=ml.EstimatorType.ML_ESTIMATOR,
        data_repository_type=repositories.DataRepositoryType.LOCAL,
        evaluator_type=ml.EvaluatorType.TIME_EVALUATOR,
        algorithm_type=ml.AlgorithmType.LIGHT_GBM,
        do_hpo=do_hpo,
    )

    scores = estimator.creat_model()

    return scores


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Train and deploy the fraud detection model."
    )
    parser.add_argument(
        "--do-hpo",
        action="store_true",
        help="If indicated, the estimator will perform hpo routine.",
    )

    args = parser.parse_args()
    if vars(args) == {}:
        parser.print_help()
        exit(1)

    main(do_hpo=args.do_hpo)
