from malaya_speech.supervised import vocoder
from herpetologist import check_type

_melgan_availability = {
    'male': {
        'Size (MB)': 17.3,
        'Quantized Size (MB)': 4.53,
        'Mel loss': 0.4443,
    },
    'female': {
        'Size (MB)': 17.3,
        'Quantized Size (MB)': 4.53,
        'Mel loss': 0.4434,
    },
    'husein': {
        'Size (MB)': 17.3,
        'Quantized Size (MB)': 4.53,
        'Mel loss': 0.4442,
    },
    'haqkiem': {
        'Size (MB)': 17.3,
        'Quantized Size (MB)': 4.53,
        'Mel loss': 0.4819,
    },
    'yasmin': {
        'Size (MB)': 17.3,
        'Quantized Size (MB)': 4.53,
        'Mel loss': 0.4867,
    },
    'osman': {
        'Size (MB)': 17.3,
        'Quantized Size (MB)': 4.53,
        'Mel loss': 0.4819,
    },
    'universal': {
        'Size (MB)': 309,
        'Quantized Size (MB)': 77.5,
        'Mel loss': 0.4463,
    },
    'universal-1024': {
        'Size (MB)': 78.4,
        'Quantized Size (MB)': 19.9,
        'Mel loss': 0.4591,
    },
    'universal-384': {
        'Size (MB)': 11.3,
        'Quantized Size (MB)': 3.06,
        'Mel loss': 0.4445,
    },
}

_mbmelgan_availability = {
    'female': {
        'Size (MB)': 10.4,
        'Quantized Size (MB)': 2.82,
        'Mel loss': 0.4356,
    },
    'male': {
        'Size (MB)': 10.4,
        'Quantized Size (MB)': 2.82,
        'Mel loss': 0.3735,
    },
    'husein': {
        'Size (MB)': 10.4,
        'Quantized Size (MB)': 2.82,
        'Mel loss': 0.4356,
    },
    'haqkiem': {
        'Size (MB)': 10.4,
        'Quantized Size (MB)': 2.82,
        'Mel loss': 0.4192,
    },
}

_hifigan_availability = {
    'male': {
        'Size (MB)': 8.8,
        'Quantized Size (MB)': 2.49,
        'Mel loss': 0.465,
    },
    'female': {
        'Size (MB)': 8.8,
        'Quantized Size (MB)': 2.49,
        'Mel loss': 0.5547,
    },
    'universal-1024': {
        'Size (MB)': 170,
        'Quantized Size (MB)': 42.9,
        'Mel loss': 0.3346,
    },
    'universal-768': {
        'Size (MB)': 72.8,
        'Quantized Size (MB)': 18.5,
        'Mel loss': 0.3617,
    },
    'universal-512': {
        'Size (MB)': 32.6,
        'Quantized Size (MB)': 8.6,
        'Mel loss': 0.3253,
    },
}


def available_melgan():
    """
    List available MelGAN Mel-to-Speech models.
    """
    from malaya_speech.utils import describe_availability

    return describe_availability(_melgan_availability)


def available_mbmelgan():
    """
    List available Multiband MelGAN Mel-to-Speech models.
    """
    from malaya_speech.utils import describe_availability

    return describe_availability(_mbmelgan_availability)


def available_hifigan():
    """
    List available HiFiGAN Mel-to-Speech models.
    """
    from malaya_speech.utils import describe_availability

    return describe_availability(_hifigan_availability)


@check_type
def melgan(model: str = 'universal-1024', quantized: bool = False, **kwargs):
    """
    Load MelGAN Vocoder model.

    Parameters
    ----------
    model : str, optional (default='universal-1024')
        Model architecture supported. Allowed values:

        * ``'female'`` - MelGAN trained on female voice.
        * ``'male'`` - MelGAN trained on male voice.
        * ``'husein'`` - MelGAN trained on Husein voice, https://www.linkedin.com/in/husein-zolkepli/
        * ``'haqkiem'`` - MelGAN trained on Haqkiem voice, https://www.linkedin.com/in/haqkiem-daim/
        * ``'yasmin'`` - MelGAN trained on female Yasmin voice.
        * ``'osman'`` - MelGAN trained on male Osman voice.
        * ``'female-singlish'`` - MelGAN trained on Female Singlish voice, https://www.imda.gov.sg/programme-listing/digital-services-lab/national-speech-corpus
        * ``'universal'`` - Universal MelGAN trained on multiple speakers.
        * ``'universal-1024'`` - Universal MelGAN with 1024 filters trained on multiple speakers.
        * ``'universal-384'`` - Universal MelGAN with 384 filters trained on multiple speakers.

    quantized : bool, optional (default=False)
        if True, will load 8-bit quantized model.
        Quantized model not necessary faster, totally depends on the machine.

    Returns
    -------
    result : malaya_speech.model.synthesis.Vocoder class
    """
    model = model.lower()
    if model not in _melgan_availability:
        raise ValueError(
            'model not supported, please check supported models from `malaya_speech.vocoder.available_melgan()`.'
        )

    return vocoder.load(
        model=model,
        module='vocoder-melgan',
        quantized=quantized,
        **kwargs
    )


@check_type
def mbmelgan(model: str = 'female', quantized: bool = False, **kwargs):
    """
    Load Multiband MelGAN Vocoder model.

    Parameters
    ----------
    model : str, optional (default='female')
        Model architecture supported. Allowed values:

        * ``'female'`` - MBMelGAN trained on female voice.
        * ``'male'`` - MBMelGAN trained on male voice.
        * ``'husein'`` - MBMelGAN trained on Husein voice, https://www.linkedin.com/in/husein-zolkepli/
        * ``'haqkiem'`` - MBMelGAN trained on Haqkiem voice, https://www.linkedin.com/in/haqkiem-daim/

    quantized : bool, optional (default=False)
        if True, will load 8-bit quantized model.
        Quantized model not necessary faster, totally depends on the machine.

    Returns
    -------
    result : malaya_speech.model.synthesis.Vocoder class
    """
    model = model.lower()
    if model not in _mbmelgan_availability:
        raise ValueError(
            'model not supported, please check supported models from `malaya_speech.vocoder.available_mbmelgan()`.'
        )
    return vocoder.load(
        model=model,
        module='vocoder-mbmelgan',
        quantized=quantized,
        **kwargs
    )


@check_type
def hifigan(model: str = 'universal-768', quantized: bool = False, **kwargs):
    """
    Load HiFiGAN Vocoder model.

    Parameters
    ----------
    model : str, optional (default='universal-768')
        Model architecture supported. Allowed values:

        * ``'female'`` - HiFiGAN trained on female voice.
        * ``'male'`` - HiFiGAN trained on male voice.
        * ``'universal-1024'`` - Universal HiFiGAN with 1024 filters trained on multiple speakers.
        * ``'universal-768'`` - Universal HiFiGAN with 768 filters trained on multiple speakers.
        * ``'universal-512'`` - Universal HiFiGAN with 512 filters trained on multiple speakers.

    quantized : bool, optional (default=False)
        if True, will load 8-bit quantized model.
        Quantized model not necessary faster, totally depends on the machine.

    Returns
    -------
    result : malaya_speech.model.synthesis.Vocoder class
    """
    model = model.lower()
    if model not in _hifigan_availability:
        raise ValueError(
            'model not supported, please check supported models from `malaya_speech.vocoder.available_hifigan()`.'
        )
    return vocoder.load(
        model=model,
        module='vocoder-hifigan',
        quantized=quantized,
        **kwargs
    )
