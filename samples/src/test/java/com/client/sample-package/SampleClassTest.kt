package com.client.sample-package

class SampleClassTest : BaseTest() {

    private lateinit var subject: SampleClass

    private val mockedSampleDependency: SampleDependency = mockk()

    @Before
    fun setUp() {
        clearAllMocks()
        subject = SampleClass(
            mockedSampleDependency,
        )
    }

    @Test
    fun `placeholder test`() = runTest {
    
    }
}