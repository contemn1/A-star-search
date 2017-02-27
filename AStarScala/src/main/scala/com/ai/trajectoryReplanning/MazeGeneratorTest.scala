package com.ai.trajectoryReplanning

import scala.collection.mutable

/**
  * Created by zxj on 2017/2/19.
  */
object MazeGeneratorTest {

  def initCellMatrix(size: Int) = {
    val matrix = Array.ofDim[MazeCell](size, size)
    matrix.map(array => array.map(_ => new MazeCell()))
  }

  def showResult(search: ((Int, Int), (Int, Int)) => SearchResult, start:(Int, Int), end: (Int, Int)): Unit = {
    val result = search(start, end)
    val succeed = result.success
    val resultMap = result.sourceMap
    if (succeed) {

      val resultList = getResultPath(end, resultMap)
      println(resultList.size)
      resultList.foreach(tuple => print(tuple + "-> "))
    }
  }

  def getResultPath(resultPoint: (Int, Int), sourceMap: mutable.Map[(Int, Int), (Int, Int)]) = {
    def mapToList(
      startPoint: (Int, Int),
      sourceMap: mutable.Map[(Int, Int), (Int, Int)],
      resultList: List[(Int, Int)]): List[(Int, Int)] = {
      val ancestorPoint = sourceMap.get(startPoint)
      if (ancestorPoint.isEmpty) {
        return resultList
      }
      mapToList(ancestorPoint.get, sourceMap, ancestorPoint.get :: resultList)
    }
    mapToList(resultPoint, sourceMap, List[(Int, Int)](resultPoint))
  }

  def tupleEqual(first: (Int, Int), second: (Int, Int)) = first._1 == second._1 && first._2 == second._2


  def main (args: Array[String]): Unit = {
    val firstMatrix = initCellMatrix(101)
    val generator = new MazeGenerator(firstMatrix)
    generator.generateBlcoks()
    showResult(generator.adaptiveAStar(5), (0, 0), (10, 0))
  }
}
