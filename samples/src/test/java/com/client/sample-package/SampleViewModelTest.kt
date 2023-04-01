package com.client.sample-package

class SampleViewModelTest : BaseTest() {

    private lateinit var subject: SampleViewModel

    private val mockedSampleDependency: SampleDependency = mockk()

    @Before
    fun setUp() {
        clearAllMocks()
        subject = SampleViewModel(
            mockedSampleDependency
        )
    }

    @Test
    fun `placeholder test`() = runTest {
    
    }
}