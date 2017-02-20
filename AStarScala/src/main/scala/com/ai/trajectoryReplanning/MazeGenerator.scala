package com.ai.trajectoryReplanning

import scala.annotation.tailrec
import scala.collection.mutable
import scala.util.Random

/**
  * Created by zxj on 2017/2/19.
  */
class MazeGenerator(cellMatrix: Array[Array[MazeCell]]) {
  val blockArray = Array(true, false, true, true, false, false, false, false, false, false)
  var cellVisited = 0
  val directions = List((0, 1), (0, -1), (1, 0), (-1, 0))

  def getBlocked = blockArray(Random.nextInt(blockArray.length))

  def neibours(point : (Int, Int), directionList: List[(Int, Int)]) = {
    val (x, y) = point
    directionList.map(tuple => (tuple._1 + x, tuple._2 + y))
      .filter(tuple => withinBound(tuple))
  }

  def withinBound(point: (Int, Int), matrix: Array[Array[MazeCell]] = cellMatrix): Boolean = {
    point._1 >= 0 && point._1 < matrix.length && point._2 >= 0 && point._2 < matrix(point._1).length
  }

  def manhatanDistance(start: (Int, Int), end: (Int, Int)) = Math.abs(end._1 - start._1) + Math.abs(end._2 - start._2)

  def herrustic(start: (Int, Int), end:(Int, Int)) = {
    if (isWall(start) || isWall(end)) Int.MaxValue else manhatanDistance(start, end)
  }

  def isWall(point: (Int, Int)) = {
    val (x, y) = point
    cellMatrix(x)(y).blocked
  }

  @tailrec
  private def visitCell(cell: (Int, Int)): Unit = {
    val currentCell = cellMatrix(cell._1)(cell._2)
    cellVisited += 1
    currentCell.visited = true
    val neibourCells = neibours(cell, directions)
      .filter(location => !cellMatrix(location._1)(location._2).visited)
      .map { location =>
        cellMatrix(location._1)(location._2).blocked = getBlocked
        location
      }.filter(location => !cellMatrix(location._1)(location._2).blocked)
    if (neibourCells.isEmpty) {
      return
    }
      val nextCell = neibourCells(Random.nextInt(neibourCells.length))
      visitCell(nextCell)
    }

  def transform(cellMatrix: Array[Array[MazeCell]] = cellMatrix) = {
    cellMatrix
      .map(array => array.map(cell => if (cell.blocked) 1 else 0))
      .foreach { array =>
        val res = array.foldLeft(" ")((current, next) => current + "\t" + next.toString)
        println(res)
      }
  }


  def generateBlcoks(): Unit ={
    while (cellVisited != cellMatrix.size * cellMatrix.size) {
      val randomX = Random.nextInt(cellMatrix.size)
      val randomY = Random.nextInt(cellMatrix.size)
      if (!cellMatrix(randomX)(randomY).visited) {
        visitCell((randomX, randomY))
      }
    }
  }

  def aStarSearch(start: (Int, Int), goal: (Int, Int)) = {
    @tailrec
    def pathFinder(
      frontier: mutable.PriorityQueue[CellInformation],
      sourceMap: mutable.Map[(Int, Int), (Int, Int)],
      costSoFar: mutable.Map[(Int, Int), Int]): (Boolean, mutable.Map[(Int, Int), (Int, Int)]) = {
      if (frontier.isEmpty) {
        return (false, sourceMap)
      }
      val current = frontier.dequeue()
      if (current.location equals  goal) {
        return (true, sourceMap)
      }
      neibours(current.location, directions).foreach { next =>
        val newCost = costSoFar(current.location) + manhatanDistance(current.location, next)
        val oldCost = costSoFar.get(next)
        if (oldCost.isEmpty || newCost < oldCost.get) {
          costSoFar(next) = newCost
          val priority = newCost + herrustic(goal, next)
          frontier.enqueue(new CellInformation(next, priority))
          sourceMap(next) = current.location
        }
      }
      pathFinder(frontier, sourceMap, costSoFar)
    }

    var frontier =  mutable.PriorityQueue.empty(MinOrder)
    frontier += CellInformation(start, 0)
    val sourceMap = new mutable.HashMap[(Int, Int), (Int, Int)]()
    var costSoFar = new mutable.HashMap[(Int, Int), Int]()
    costSoFar += start -> 0
    pathFinder(frontier, sourceMap, costSoFar)
  }

  def printResult(resultPoint: (Int, Int), sourceMap: mutable.Map[(Int, Int), (Int, Int)]) = {
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
}

object MinOrder extends Ordering[CellInformation] {
  def compare(x:CellInformation, y:CellInformation) = y.fScore compare x.fScore
}

case class CellInformation(location: (Int, Int), fScore: Int)