import * as cp from "child_process"

export const pythonProcess1 = cp.spawn('python',["./crawl/requestMain.py"])
export const pythonProcess2 = cp.spawn('python',["/crawl/requestMain.py","배터리",100])
export const pythonProcess3 = cp.spawn('python',["./crawl/requestMain.py","바나듐이온배터리",100])