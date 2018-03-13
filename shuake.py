# -*- coding=utf-8 -*-
import requests
import json
import time
from moviepy.editor import VideoFileClip
getprofile='http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/system/getProfile'
getunitdetial='http://student.zjedu.moocollege.com/nodeapi/3.0.1/teacher/course/plan/unit/getDetail'
getinfo='http://student.zjedu.moocollege.com/nodeapi/3.0.1/common/ccPlayer/getInfo'
listurl='http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/system/list'
sessionlist='http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/plan/list'
loginurl='http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/system/login'
upurl='http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/uploadLearnRate'
listrequest='{"status": "", "search": "", "current": 1, "pageSize": 12}'
headers={
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
'Content-Length':'97',
'Content-Type':'application/json',
'Cookie':'Hm_lvt_ffe6480e8f1f8d0097c02b901ba4030e=1520920186; Hm_lpvt_ffe6480e8f1f8d0097c02b901ba4030e=1520920186; NOISSESUDEJZXJ=s%3A-XlHly_pQbxsudr6PC_x1xIRZwMMdSvs.jprYBFGTycFMOIXQEEjrsOr9PT%2BJixNhSYjy%2FyRrZ7A; Hm_lvt_70a5d649dfa86aee3afdc28e95ee2c41=1520920214; ccPlayer-MediaType-zjedu=%22html5%22; avatar-student-zjedu=%22%22; Hm_lpvt_70a5d649dfa86aee3afdc28e95ee2c41=1520946321; token-student-zjedu=%229f40fe13-ba31-497f-a5f6-3982cd20f4a3%22; realname-student-zjedu=%22%E5%BC%A0%E4%B9%A6%E6%80%A1%22',
'DNT':'1',
'Host':'student.zjedu.moocollege.com',
'Origin':'http://student.zjedu.moocollege.com',
'Referer':'http://student.zjedu.moocollege.com/system/login',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3355.4 Safari/537.36'
}
if __name__ == '__main__':
	session=requests.session()
	session.headers = headers
	username=str(input('请输入学号，回车结束:  ——>'))
	password=str(input('请输入密码，回车结束: ——>'))
	# username=''
	# password = ''

	userdata=json.loads('{"orgId": 64, "username": "'+ username+'", "password": "'+password+'", "type": "studentNo", "rememberMe": false}')
	print('登录中...',end='\n\n')
	res=session.post(loginurl,json=userdata)
	res=session.post(listurl,json=json.loads(listrequest))
	t=json.loads(res.content)
	courselist={}
	coursename=[]
	kc=t['data']['dataList']
	for i in kc:
		courselist[i['title']]=i['id']
		coursename.append(i['title'])

	for j in range(0,len(coursename)):
		print(str(j)+':'+coursename[j])
	xh=int(input('请输入课程序号,回车结束: ——>'))
	couseid=str(courselist[coursename[xh]])
	unitlist=session.post(sessionlist,json=json.loads('{"courseId":"'+couseid+'"}'))
	unitlist=json.loads(unitlist.content)
	unitidlist=[]
	for i in unitlist['data']:
		for j in i['data']:
			for k in j['data']:
				if k['status']<2:
					unitidlist.append(k['unitId'])
	if len(unitidlist)>0:
		print('章节代码：'+str(unitidlist),end='\n\n')
		for i in unitidlist:
			unitid=str(i)
			res=session.post(getunitdetial,json=json.loads('{"unitId":'+unitid+'}'))
			detail=json.loads(res.content)
			videoId=detail['data']['data']['videoId']
			if videoId=='null':
				continue
			res=session.post(getinfo,json=json.loads('{"id":"'+str(videoId)+'"}'))
			source=json.loads(res.content)
			source=source['data']['sources'][0]
			print('读取视频时长，请稍后')
			clip=VideoFileClip(source)
			duration=int(clip.duration)
			print('视频时长:'+str(duration)+'秒')

			for i in range(0,int(duration/20)+1):
				uploaddata=json.loads('{"unitId": "'+unitid+'", "courseId": "'+couseid+'", "playPosition": '+str(i*20)+'}')
				t=session.post(upurl,json=uploaddata)
				print('requests: '+str(uploaddata))
				print('respone: '+t.text,end='\n\n')
				time.sleep(1.5)
			time.sleep(1.5)
			uploaddata=json.loads('{"unitId": "'+unitid+'", "courseId": "'+couseid+'", "playPosition": '+str(duration)+'}')
			t=session.post(upurl,json=uploaddata)
			print('requests: '+str(uploaddata))
			print(t.text,end='\n')
	else:
		print('该课程已学完',end='\n\n')