package com.client.sample-package

class BasicClassTest : BaseTest() {

    private lateinit var subject: BasicClass

    private val mockedSampleDependency: SampleDependency = mockk()

    @Before
    fun setUp() {
        clearAllMocks()
        subject = BasicClass(
            mockedSampleDependency,
        )
    }

    @Test
    fun `placeholder test`() = runTest {
    
    }
}