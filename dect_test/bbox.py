def ID_Score(bboxes, class_IDs, scores, dataclass): #, txt_fname 加在要求傳入參數最後一項
	#轉換ndarray到一般array
	if isinstance(class_IDs, mx.nd.NDArray) and isinstance(scores, mx.nd.NDArray):
		bboxes1 = bboxes.asnumpy()
		cls_id = class_IDs.asnumpy()
		scores1 = scores.asnumpy()
	flage = 2
	for r in range(len(cls_id)):
		if float(scores1[-1][r])<0.5:break
		if int(cls_id[r])==0:flage=0
		elif int(cls_id[r])==1:flage=1
		elif int(cls_id[r])==2:flage=2
		elif int(cls_id[r])==3:flage=3
		elif int(cls_id[r])==4:flage=4
	if flage!=2:
		#f = open(aft_txt+txt_fname, 'w')
		pass
	else:return 0
	#比較class, score
	for r in range(len(cls_id)):
		if float(scores1[-1][r])<0.5:break
		xmin = int(bboxes1[0][0])
		ymin = int(bboxes1[0][1])
		xmax = int(bboxes1[0][2])
		ymax = int(bboxes1[0][3])
		f.write(dataclass[int(cls_id[r])]+' '+str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)+'\n')
		#print(dataclass[int(cls_id[r])], str(scores1[-1][r]), str(bboxes1[0][0]), str(bboxes1[0][1]))
	f.close()
	return 1

def ab123():
    return 0
