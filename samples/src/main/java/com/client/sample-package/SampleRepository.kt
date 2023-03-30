package com.client.sample-package

class SampleRepository @Inject constructor(
    private val sampleDependency: SampleDependency,
    private val dispatcher: CoroutineDispatcher,
) {

}