from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import people_also_ask
import people_also_ask_it
# from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
def remove_date(answer):
	months = ['.Jan', '.Feb', '.Mar', '.Apr',
			'.May', '.Jun', '.Jul', '.Aug',
			'.Sep', '.Oct', '.Nov', '.Dec']
	for month in months:
		month_index = answer.find(month)
		if month_index != -1:
			answer = answer[:month_index + 1]
			break
	return answer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_google(request):
	keyword = request.GET['keyword']
	get_answers = request.GET['get_answers']
	limit = int(request.GET['limit'])
	remReq = int(request.GET['remReq'])
	remDays = int(request.GET['remDays'])
	try:
		answers = []
		questions = people_also_ask.get_related_questions(keyword, limit)
		for i in range(len(questions)):
			questions[i] = questions[i].split('?')[0] + '?'
			if get_answers == 'true':
				answer = people_also_ask.get_simple_answer(questions[i])
				answer = remove_date(answer)
				answers.append(answer)
		if get_answers == 'true':
			return Response({'Questions':questions, 'Answers': answers,
								'RemainingRequests':remReq,
								'RemainingDays':remDays}, status=status.HTTP_200_OK)
		else:
			return Response({'Questions':questions,
								'RemainingRequests':remReq,
								'RemainingDays':remDays}, status=status.HTTP_200_OK)
	except Exception as e:
		try:
			answers = []
			questions = people_also_ask_it.get_related_questions(keyword, limit)
			for i in range(len(questions)):
				questions[i] = questions[i].split('?')[0] + '?'
				if get_answers == 'true':
					answer = people_also_ask_it.get_simple_answer(questions[i])
					answer = remove_date(answer)
					answers.append(answer)
			if get_answers == 'true':
				return Response({'Questions':questions, 'Answers': answers,
									'RemainingRequests':remReq,
									'RemainingDays':remDays}, status=status.HTTP_200_OK)
			else:
				return Response({'Questions':questions,
									'RemainingRequests':remReq,
									'RemainingDays':remDays}, status=status.HTTP_200_OK)
		except Exception as e:
			return Response({'Questions': 'No questions got.',
								'Answers': 'No Answers were found',
								'RemainingRequests':remReq,
								'RemainingDays': remDays}, status=status.HTTP_400_BAD_REQUEST)
