from db.db_connection import get_sentences

SENTENCES_IN_PARAGRAPH = 4

def get_reuters_paragraph(ids, count):
	ids_required = count * SENTENCES_IN_PARAGRAPH
	ids = ids[:ids_required]

	sentences = []
	try:
		sentences = get_sentences(ids)
	except(e):
		print 'Topic not supported'

	if not sentences:
		return []

	paragraphs = []
	for i in range(count):
		text = ''
		for j in range(SENTENCES_IN_PARAGRAPH):
			sentence = sentences.pop()
			if not sentence:
				continue
			text += ' ' + sentence[0][0]
		paragraphs.append(text)
	return paragraphs