package com.client.sample-package

@AndroidEntryPoint
class SampleFragment : Fragment(R.layout.fragment_sample) {

    private val viewModel: SampleViewModel by viewModels()

    private var viewBinding: FragmentSampleBinding? = null

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val binding = FragmentSampleBinding.bind(view)
        viewBinding = binding
    }

    override fun onDestroyView() {
        fragmentBlankBinding = null
        super.onDestroyView()
    }
}