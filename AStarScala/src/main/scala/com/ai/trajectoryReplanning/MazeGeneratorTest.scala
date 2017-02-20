package com.ai.trajectoryReplanning

/**
  * Created by zxj on 2017/2/19.
  */
object MazeGeneratorTest {

  def initCellMatrix(size: Int) = {
    val matrix = Array.ofDim[MazeCell](size, size)
    matrix.map(array => array.map(_ => new MazeCell()))
  }


  def main (args: Array[String]): Unit = {
    val firstMatrix = initCellMatrix(101)
    val generator = new MazeGenerator(firstMatrix)
    generator.generateBlcoks()
    val (succeed, resultMap) = generator.aStarSearch((3,5), (30,20))
    if (succeed) {
      val resultList = generator.printResult((30, 20), resultMap)
      resultList.foreach(tuple => print(tuple + "-> "))
    }
  }
}
