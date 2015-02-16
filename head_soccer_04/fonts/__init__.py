import pygame

pygame.font.init()

path = "fonts/"

VCR_OSD_MONO = dict()
VCR_OSD_MONO["15"] = pygame.font.Font(path+"VCR_OSD_MONO.ttf",15)
VCR_OSD_MONO["20"] = pygame.font.Font(path+"VCR_OSD_MONO.ttf",20)
VCR_OSD_MONO["25"] = pygame.font.Font(path+"VCR_OSD_MONO.ttf",25)
VCR_OSD_MONO["30"] = pygame.font.Font(path+"VCR_OSD_MONO.ttf",30)
VCR_OSD_MONO["35"] = pygame.font.Font(path+"VCR_OSD_MONO.ttf",35)
VCR_OSD_MONO["40"] = pygame.font.Font(path+"VCR_OSD_MONO.ttf",40)

def GetFont(font):
    if font[:3] == "VOM":
	return VCR_OSD_MONO[font[4:]] 
