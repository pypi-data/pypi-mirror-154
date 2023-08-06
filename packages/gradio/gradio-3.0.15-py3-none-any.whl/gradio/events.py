from __future__ import annotations

from typing import TYPE_CHECKING, Any, AnyStr, Callable, Dict, List, Optional, Tuple

from gradio.blocks import Block

if TYPE_CHECKING:  # Only import for type checking (is False at runtime).
    from gradio.components import Component, StatusTracker


class Changeable(Block):
    def change(
        self,
        fn: Callable,
        inputs: List[Component],
        outputs: List[Component],
        status_tracker: Optional[StatusTracker] = None,
        api_name: AnyStr = None,
        queue: Optional[bool] = None,
        _js: Optional[str] = None,
        _preprocess: bool = True,
        _postprocess: bool = True,
    ):
        """
        Parameters:
            fn: Callable function
            inputs: List of inputs
            outputs: List of outputs
            status_tracker: StatusTracker to visualize function progress
            api_name: Defining this parameter exposes the endpoint in the api docs
            _js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of input and outputs components, return should be a list of values for output component.
        Returns: None
        """
        self.set_event_trigger(
            "change",
            fn,
            inputs,
            outputs,
            status_tracker=status_tracker,
            api_name=api_name,
            js=_js,
            preprocess=_preprocess,
            postprocess=_postprocess,
            queue=queue,
        )


class Clickable(Block):
    def click(
        self,
        fn: Callable,
        inputs: List[Component],
        outputs: List[Component],
        status_tracker: Optional[StatusTracker] = None,
        api_name: AnyStr = None,
        queue=None,
        _js: Optional[str] = None,
        _preprocess: bool = True,
        _postprocess: bool = True,
    ):
        """
        Parameters:
            fn: Callable function
            inputs: List of inputs
            outputs: List of outputs
            status_tracker: StatusTracker to visualize function progress
            api_name: Defining this parameter exposes the endpoint in the api docs
            _js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            _preprocess: If False, will not run preprocessing of component data before running 'fn'.
            _postprocess: If False, will not run postprocessing of component data before returning 'fn' output.
        Returns: None
        """
        self.set_event_trigger(
            "click",
            fn,
            inputs,
            outputs,
            status_tracker=status_tracker,
            api_name=api_name,
            queue=queue,
            js=_js,
            preprocess=_preprocess,
            postprocess=_postprocess,
        )


class Submittable(Block):
    def submit(
        self,
        fn: Callable,
        inputs: List[Component],
        outputs: List[Component],
        status_tracker: Optional[StatusTracker] = None,
        api_name: AnyStr = None,
        queue: Optional[bool] = None,
        _js: Optional[str] = None,
        _preprocess: bool = True,
        _postprocess: bool = True,
    ):
        """
        Parameters:
            fn: Callable function
            inputs: List of inputs
            outputs: List of outputs
            status_tracker: StatusTracker to visualize function progress
            api_name: Defining this parameter exposes the endpoint in the api docs
            _js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
        Returns: None
        """
        self.set_event_trigger(
            "submit",
            fn,
            inputs,
            outputs,
            status_tracker=status_tracker,
            api_name=api_name,
            js=_js,
            preprocess=_preprocess,
            postprocess=_postprocess,
            queue=queue,
        )


class Editable(Block):
    def edit(
        self,
        fn: Callable,
        inputs: List[Component],
        outputs: List[Component],
        api_name: AnyStr = None,
        queue: Optional[bool] = None,
        _js: Optional[str] = None,
        _preprocess: bool = True,
        _postprocess: bool = True,
    ):
        """
        Parameters:
            fn: Callable function
            inputs: List of inputs
            outputs: List of outputs
            api_name: Defining this parameter exposes the endpoint in the api docs
            _js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
        Returns: None
        """
        self.set_event_trigger(
            "edit",
            fn,
            inputs,
            outputs,
            api_name=api_name,
            js=_js,
            preprocess=_preprocess,
            postprocess=_postprocess,
            queue=queue,
        )


class Clearable(Block):
    def clear(
        self,
        fn: Callable,
        inputs: List[Component],
        outputs: List[Component],
        api_name: AnyStr = None,
        queue: Optional[bool] = None,
        _js: Optional[str] = None,
        _preprocess: bool = True,
        _postprocess: bool = True,
    ):
        """
        Parameters:
            fn: Callable function
            inputs: List of inputs
            outputs: List of outputs
            api_name: Defining this parameter exposes the endpoint in the api docs
            _js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
        Returns: None
        """
        self.set_event_trigger(
            "submit",
            fn,
            inputs,
            outputs,
            api_name=api_name,
            js=_js,
            preprocess=_preprocess,
            postprocess=_postprocess,
            queue=queue,
        )


class Playable(Block):
    def play(
        self,
        fn: Callable,
        inputs: List[Component],
        outputs: List[Component],
        api_name: AnyStr = None,
        queue: Optional[bool] = None,
        _js: Optional[str] = None,
        _preprocess: bool = True,
        _postprocess: bool = True,
    ):
        """
        Parameters:
            fn: Callable function
            inputs: List of inputs
            outputs: List of outputs
            api_name: Defining this parameter exposes the endpoint in the api docs
            _js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
        Returns: None
        """
        self.set_event_trigger(
            "play",
            fn,
            inputs,
            outputs,
            api_name=api_name,
            js=_js,
            preprocess=_preprocess,
            postprocess=_postprocess,
            queue=queue,
        )

    def pause(
        self,
        fn: Callable,
        inputs: List[Component],
        outputs: List[Component],
        api_name: Optional[AnyStr] = None,
        queue: Optional[bool] = None,
        _js: Optional[str] = None,
        _preprocess: bool = True,
        _postprocess: bool = True,
    ):
        """
        Parameters:
            fn: Callable function
            inputs: List of inputs
            outputs: List of outputs
            api_name: Defining this parameter exposes the endpoint in the api docs
            _js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
        Returns: None
        """
        self.set_event_trigger(
            "pause",
            fn,
            inputs,
            outputs,
            api_name=api_name,
            js=_js,
            preprocess=_preprocess,
            postprocess=_postprocess,
            queue=queue,
        )

    def stop(
        self,
        fn: Callable,
        inputs: List[Component],
        outputs: List[Component],
        api_name: AnyStr = None,
        queue: Optional[bool] = None,
        _js: Optional[str] = None,
        _preprocess: bool = True,
        _postprocess: bool = True,
    ):
        """
        Parameters:
            fn: Callable function
            inputs: List of inputs
            outputs: List of outputs
            api_name: Defining this parameter exposes the endpoint in the api docs
            _js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
        Returns: None
        """
        self.set_event_trigger(
            "stop",
            fn,
            inputs,
            outputs,
            api_name=api_name,
            js=_js,
            preprocess=_preprocess,
            postprocess=_postprocess,
            queue=queue,
        )


class Streamable(Block):
    def stream(
        self,
        fn: Callable,
        inputs: List[Component],
        outputs: List[Component],
        api_name: AnyStr = None,
        queue: Optional[bool] = None,
        _js: Optional[str] = None,
        _preprocess: bool = True,
        _postprocess: bool = True,
    ):
        """
        Parameters:
            fn: Callable function
            inputs: List of inputs
            outputs: List of outputs
            api_name: Defining this parameter exposes the endpoint in the api docs
            _js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
        Returns: None
        """
        self.streaming = True
        self.set_event_trigger(
            "stream",
            fn,
            inputs,
            outputs,
            api_name=api_name,
            js=_js,
            preprocess=_preprocess,
            postprocess=_postprocess,
            queue=queue,
        )
