import openai
import json
import tiktoken
import os
from halo import Halo

openai.api_key = os.getenv("OPEN_AI_KEY")

def rule_set() -> str:
    return """
        // Kotlin

        // Sample Fragment
        package com.client.app

        @AndroidEntryPoint
        class SampleFragment : Fragment(R.layout.fragment_sample) {
        
            private val viewModel: SampleViewModel by viewModels()

            private var viewBinding: FragmentSampleBinding? = null

            override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
                super.onViewCreated(view, savedInstanceState)
                val binding = FragmentSampleBinding.bind(view)
                fragmentBlankBinding = binding
            }

            override fun onDestroyView() {
                fragmentBlankBinding = null
                super.onDestroyView()
            }
        }

        // Sample Fragment Test Suite
        package com.client.app

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

        // Sample ViewModel
        package com.client.app

        @HiltViewModel
        internal class SampleViewModel @Inject constructor(
            private val sampleDependency: SampleDependency,
        ) : ViewModel() {
        
        }

        // Sample ViewModel Test Suite
        package com.client.app

        internal class SampleViewModelTest : BaseTest() {

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

        // Sample Repository
        package com.client.app

        internal class SampleRepository @Inject constructor(
            private val sampleDependency: SampleDependency,
            private val dispatcher: CoroutineDispatcher,
        ) {
        
        }

        // Sample Repository Test Suite
        package com.client.app

        internal class SampleRepositoryTest : BaseTest() {

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

        // Sample Class
        package com.client.app

        internal SampleClass @Inject constructor(
            private val sampleDependency: SampleDependency
        ) {
        
        }
        
        // Basic Class Test Suite
        package com.client.app

        internal class BasicClassTest : BaseTest() {

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
        **/
    """

def code_gen(rule_set: str, prompt: str) -> str:
    return f"""
    {rule_set}

    {prompt}
    """

def num_tokens_from_string(string: str, model: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens

prompt = code_gen(
    rule_set = rule_set(),
    prompt = """
        create sign in fragment.
        create authentication viewmodel.
        create authentication repository.
        create authentication service.
    """
)

model = "text-davinci-003"
max_request_tokens = 4097

num_tokens = num_tokens_from_string(prompt, model)
max_tokens = max_request_tokens - num_tokens

print(f"MAX TOKENS: {max_tokens}")

spinner = Halo(text = "Generating Code", spinner = "dots")
spinner.start()

response = openai.Completion.create(
    model = model, 
    prompt = prompt,
    temperature = 0,
    max_tokens = max_tokens
)

spinner.stop()

print(response["choices"][0]["text"])