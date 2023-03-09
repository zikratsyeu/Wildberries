import asyncio
import openpyxl
import aiohttp
from aiohttp import ClientSession
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.utils import get_product_info


class WildberriesProductView(View):
    async def get_product_data(self, session: ClientSession, article: int) -> dict:
        async with session.get(f'https://www.wildberries.ru/ajax/card/getCardData?id={article}') as response:
            data = await response.json()
            brand = data['brand']
            title = data['title']
            return {'article': article, 'brand': brand, 'title': title}

    async def post(self, request):
        data = request.POST
        if 'file' in data:
            file = request.FILES['file']
            workbook = openpyxl.load_workbook(file)
            worksheet = workbook.active
            rows = worksheet.rows
            next(rows)  # skip header
            articles = [row[0].value for row in rows]
        elif 'article' in data:
            articles = [data['article']]
        else:
            return JsonResponse({'error': 'No input provided.'})

        async with aiohttp.ClientSession() as session:
            tasks = []
            for article in articles:
                tasks.append(self.get_product_data(session, article))
            results = await asyncio.gather(*tasks)
            return JsonResponse(results, status=200)


@csrf_exempt
def article_view(request):
    if request.method == 'POST':
        article = request.POST.get('article')
        product_info = get_product_info(article)
        return JsonResponse(product_info)


@csrf_exempt
def file_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        product_infos = []
        for line in file:
            article = line.strip().decode('utf-8')
            product_info = get_product_info(article)
            product_infos.append(product_info)
        return JsonResponse(product_infos, safe=False)
