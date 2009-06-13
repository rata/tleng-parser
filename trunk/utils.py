#!/usr/bin/env python
#coding: utf8

def reverse_dict(d):
	"""Toma un diccionario que no existen distintas keys con el mismo value
	(lo asume) y devuelve un diccionario que va de values a keys. """

	reverse = {}
	for key in d.keys():
		reverse[d[key]] = key
	return reverse
