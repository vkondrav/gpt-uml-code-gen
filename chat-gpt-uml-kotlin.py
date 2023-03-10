import openai
import json
import tiktoken
import os

openai.api_key = os.getenv("OPEN_AI_KEY")

def rule_set(package: str) -> str:
    return """
        // Kotlin

        // Sample Fragment
        // file_name: SampleFragment.kt
        // file_path: src/main/java/com/client/{package}
        package com.client.{package}

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
        // file_name: SampleFragmentTest.kt
        // file_path: src/test/java/com/client/{package}
        package com.client.{package}

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
        // file_name: SampleViewModel.kt
        // file_path: src/main/java/com/client/{package}
        package com.client.{package}

        @HiltViewModel
        internal class SampleViewModel @Inject constructor(
            private val sampleDependency: SampleDependency,
        ) : ViewModel() {
        
        }

        // Sample ViewModel Test Suite
        // file_name: SampleViewModelTest.kt
        // file_path: src/test/java/com/client/{package}
        package com.client.{package}

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
        // file_name: SampleRepository.kt
        // file_path: src/main/java/com/client/{package}
        package com.client.{package}

        internal class SampleRepository @Inject constructor(
            private val sampleDependency: SampleDependency,
            private val dispatcher: CoroutineDispatcher,
        ) {
        
        }

        // Sample Repository Test Suite
        // file_name: SampleRepositoryTest.kt
        // file_path: src/test/java/com/client/{package}
        package com.client.{package}

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
        // file_name: SampleClass.kt
        // file_path: src/main/java/com/client/{package}
        package com.client.{package}

        internal SampleClass @Inject constructor(
            private val sampleDependency: SampleDependency
        ) {
        
        }
        
        // Basic Class Test Suite
        // file_name: BasicClassTest.kt
        // file_path: src/test/java/com/client/{package}
        package com.client.{package}

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

        /**
        Rules
        
        Create a class only if instructed to.
        A class only has a dependency if stated otherwise no dependencies.
        Every class must be created with its test suite.
        If not one of fragment, viewmodel or repository create a sample class.

        UML
        
        () denotes a shorthand. 
        Example: sampleRepository (SR) means SR now refers to sampleRepository.

        --> denotes a dependency. 
        Example: sampleViewModel --> sampleRepository means sampleViewModel dependends on sampleRepository. 
        Example: sampleFragment --> sampleViewModel means sampleFragment uses sampleViewModel.

        Format

        Format the response into a JSON array with a structure [{"file_name": "file_name.kt", "file_path": "file_path", "content": "sample_content"}].
        The whole response should only be a valid JSON array and nothing else.
        **/
    """.replace("{package}", package)

def code_gen(rule_set: str, prompt: str) -> str:
    return """
    {rule_set}

    {prompt}
    """.format(rule_set = rule_set, prompt = prompt)

def num_tokens_from_string(string: str, model: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens

prompt = code_gen(
    rule_set = rule_set(package = "auth"),
    prompt = """
        create sign in fragment (F).
        create sign in viewmodel (VM).
        create authentication repository (AR).
        F --> VM
        VM --> AR
    """
)

model = "text-davinci-003"

num_tokens = num_tokens_from_string(prompt, model)
max_tokens = 4097 - num_tokens

print("MAX TOKENS: {0}".format(max_tokens))

response = openai.Completion.create(
    model = model, 
    prompt = prompt,
    temperature = 0,
    max_tokens = max_tokens
)

code_gen = json.loads(response["choices"][0]["text"])

print(json.dumps(code_gen, indent = 4))

for file in code_gen:

    path = file["file_path"]
    name = file["file_name"]

    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + "/" + name, 'w+') as f:
        print(file["content"], file=f)