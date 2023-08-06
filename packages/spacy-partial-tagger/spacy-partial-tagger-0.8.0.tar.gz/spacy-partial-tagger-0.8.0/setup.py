# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacy_partial_tagger', 'spacy_partial_tagger.layers']

package_data = \
{'': ['*']}

install_requires = \
['allennlp>=2.9.2,<3.0.0',
 'colorlog>=6.6.0,<7.0.0',
 'conllu>=4.4.2,<5.0.0',
 'fugashi[unidic-lite]>=1.1.2,<2.0.0',
 'mojimoji>=0.0.12,<0.0.13',
 'partial-tagger>=0.6.0,<0.7.0',
 'pyknp>=0.6.1,<0.7.0',
 'pytokenizations>=0.8.4,<0.9.0',
 'spacy[ja,transformers]==3.2.4',
 'thinc>=8.0.15,<9.0.0',
 'torch>=1.11.0,<2.0.0',
 'transformers[ja]==4.17',
 'unidic-lite>=1.0.8,<2.0.0']

entry_points = \
{'spacy_architectures': ['spacy-partial-tagger.ConstrainedViterbiDecoder.v1 = '
                         'spacy_partial_tagger.layers.decoder:build_constrained_viterbi_decoder_v1',
                         'spacy-partial-tagger.LinearCRFEncoder.v1 = '
                         'spacy_partial_tagger.layers.encoder:build_linear_crf_encoder_v1',
                         'spacy-partial-tagger.MisalignedTok2VecTransformer.v1 '
                         '= '
                         'spacy_partial_tagger.layers.tok2vec_transformer:build_misaligned_tok2vec_transformer',
                         'spacy-partial-tagger.PartialTagger.v1 = '
                         'spacy_partial_tagger.tagger:build_partial_tagger_v1',
                         'spacy-partial-tagger.Tok2VecWrapper.v1 = '
                         'spacy_partial_tagger.layers.tok2vec_wrapper:build_tok2vec_wrapper'],
 'spacy_factories': ['partial_ner = '
                     'spacy_partial_tagger.pipeline:make_partial_ner'],
 'spacy_label_indexers': ['spacy-partial-tagger.TransformerLabelIndexer.v1 = '
                          'spacy_partial_tagger.label_indexers:configure_transformer_label_indexer'],
 'spacy_tokenizers': ['character_tokenizer.v1 = '
                      'spacy_partial_tagger.tokenizer:create_character_tokenizer'],
 'thinc_losses': ['spacy-partial-tagger.ExpectedEntityRatioLoss.v1 = '
                  'spacy_partial_tagger.loss:configure_ExpectedEntityRatioLoss']}

setup_kwargs = {
    'name': 'spacy-partial-tagger',
    'version': '0.8.0',
    'description': 'Sequence Tagger for Partially Annotated Dataset in spaCy',
    'long_description': '# spacy-partial-tagger\n\nThis is a CRF tagger for partially annotated dataset in spaCy. The implementation of \nthis tagger is based on Effland and Collins. (2021).\n\n## Dataset\n\nPrepare spaCy binary format file. This library expects tokenization is character-based.\nFor more detail about spaCy binary format, see [this page](https://spacy.io/api/data-formats#training).\n\n\n## Training\n\n```sh\npython -m spacy train config.cfg --output outputs --paths.train train.spacy --paths.dev dev.spacy \n```\n\n## Evaluation\n\n```sh\npython -m spacy evaluate outputs/model-best test.spacy\n```\n\n## Installation\n\n```\npip install spacy-partial-tagger\n```\n\n## References\n\n- Thomas Effland and Michael Collins. 2021. [Partially Supervised Named Entity Recognition via the Expected Entity Ratio Loss](https://aclanthology.org/2021.tacl-1.78/). _Transactions of the Association for Computational Linguistics_, 9:1320–1335.\n',
    'author': 'yasufumi',
    'author_email': 'yasufumi.taniguchi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tech-sketch/spacy-partial-tagger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
