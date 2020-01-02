# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class CardImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        image_name = '/'.join(request.url.split('/')[-2:])
        return image_name