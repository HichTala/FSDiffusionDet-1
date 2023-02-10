from detectron2.engine import EvalHook
from detectron2.evaluation.testing import flatten_results_dict
import detectron2.utils.comm as comm



class FSValidationHook(EvalHook):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def after_train(self):
        del self._func

class FSTestHook(EvalHook):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    def _do_eval(self):
        results = self._func()

        if results:
            assert isinstance(
                results, dict
            ), "Eval function must return a dict. Got {} instead.".format(results)

            flattened_results = flatten_results_dict(results)
            for k, v in flattened_results.items():
                try:
                    v = float(v)
                except Exception as e:
                    raise ValueError(
                        "[EvalHook] eval_function should return a nested dict of float. "
                        "Got '{}: {}' instead.".format(k, v)
                    ) from e
            # self.trainer.storage.put_scalars(**flattened_results, smoothing_hint=False)
            print(flattened_results)

        # Evaluation may take different time among workers.
        # A barrier make them start the next iteration together.
        comm.synchronize()

    
    def after_step(self):
        pass



