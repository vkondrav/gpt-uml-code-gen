package com.client.sample-package

@AndroidEntryPoint
class SampleFragment : Fragment(R.layout.fragment_sample) {

    private val viewModel: SampleViewModel by viewModels()

    private var viewBinding: FragmentSampleBinding? = null

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        viewBinding = FragmentSampleBinding.bind(view)
    }

    override fun onDestroyView() {
        viewBinding = null
        super.onDestroyView()
    }
}