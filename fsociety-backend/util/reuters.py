from db.db_connection import get_sentences

SENTENCES_IN_PARAGRAPH = 4

def get_reuters_paragraph(ids, count):
	ids_required = count * SENTENCES_IN_PARAGRAPH
	ids = ids[:ids_required]

	sentences = get_sentences(ids)
	print 'Senteces: ', sentences

	paragraphs = []
	for i in range(count):
		text = ''
		for j in range(SENTENCES_IN_PARAGRAPH):
			text += ' ' + sentences.pop()[0][0]
		paragraphs.append(text)
	return paragraphs