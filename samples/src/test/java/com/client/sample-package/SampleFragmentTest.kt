 package com.client.sample-package

@HiltAndroidTest
class SampleFragmentTest : BaseAndroidTest() {

    @BindValue
    @JvmField
    internal val viewModel: SampleViewModel = mockk()

    @Before
    fun setUp() {
        clearAllMocks()
    }

    @Test
    fun `placeholder test`() {
        launchFragmentInContainer<SampleFragment>() { fragment ->

        }
    }
}