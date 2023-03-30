package com.client.sample-package

@HiltViewModel
class SampleViewModel @Inject constructor(
    private val sampleDependency: SampleDependency,
) : ViewModel() {

}
