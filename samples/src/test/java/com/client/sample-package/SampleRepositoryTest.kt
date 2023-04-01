package com.client.sample-package

class SampleRepositoryTest : BaseTest() {

    private lateinit var subject: SampleRepository

    private val mockedSampleDependency: SampleDependency = mockk()

    @Before
    fun setUp() {
        clearAllMocks()
        subject = SampleRepository(
            mockedSampleDependency,
        )
    }

    @Test
    fun `placeholder test`() = runTest {
    
    }
}