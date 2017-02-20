package com.ai.trajectoryReplanning

/**
  * Created by zxj on 2017/2/19.
  */
class MazeCell(var visited: Boolean, var blocked: Boolean) {
  def this (){
    this(false, false)
  }
}
