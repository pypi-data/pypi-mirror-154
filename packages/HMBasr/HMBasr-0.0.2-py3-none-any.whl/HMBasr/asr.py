import torch
import torchaudio
from datasets import load_dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, Wav2Vec2CTCTokenizer
import ctcdecode
import numpy as np
import librosa

def transcription(audio_path):

	repo_name = "loulely/XLSR_300M_Fine_Tuning_FR_3"

	processor = Wav2Vec2Processor.from_pretrained(repo_name)
	tokenizer = Wav2Vec2CTCTokenizer.from_pretrained(repo_name)
	model = Wav2Vec2ForCTC.from_pretrained(repo_name)

	speech, rate = librosa.load(audio_path,sr=16000)

	inputs = processor(speech, sampling_rate=16_000, return_tensors="pt", padding=True)

	with torch.no_grad():
  		logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits

	predicted_ids = torch.argmax(logits, dim=-1)

	vocab_dict = tokenizer.get_vocab()
	sort_vocab = sorted((value, key) for (key,value) in vocab_dict.items())
	vocab = [x[1].replace("|", " ") if x[1] not in tokenizer.all_special_tokens else "_" for x in sort_vocab]

	vocabulary = vocab
	alpha = 2.5 # LM Weight
	beta = 0.0 # LM Usage Reward
	word_lm_scorer = ctcdecode.WordKenLMScorer('5gram_correct.arpa', alpha, beta) # use your own kenlm model
	decoder = ctcdecode.BeamSearchDecoder(
	    vocabulary,
	    num_workers=2,
	    beam_width=128,
	    scorers=[word_lm_scorer],
	    cutoff_prob=np.log(0.000001),
	    cutoff_top_n=40
	)
	text = decoder.decode_batch(logits.numpy())

	print(text)

	return