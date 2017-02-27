package com.ai.trajectoryReplanning

import scala.annotation.tailrec
import scala.collection.mutable
import scala.util.Random
import util.control.Breaks.breakable
import util.control.Breaks.break

/**
  * Created by zxj on 2017/2/19.
  */
class MazeGenerator(val cellMatrix: Array[Array[MazeCell]]) {
  val blockArray = Array(true, false, true, true, false, false, false, false, false, false)
  var cellVisited = 0
  val directions = List((0, 1), (0, -1), (1, 0), (-1, 0))
  var upperBound = -1
  def getBlocked = blockArray(Random.nextInt(blockArray.length))

  private def blcokedCell(point: (Int, Int)) = {
    val (x, y) = point
    cellMatrix(x)(y).blocked
  }

  private def neibours(point : (Int, Int), directionList: List[(Int, Int)]) = {
    val (x, y) = point
    directionList.map(tuple => (tuple._1 + x, tuple._2 + y))
      .filter(tuple => withinBound(tuple))
  }

  private def withinBound(point: (Int, Int), matrix: Array[Array[MazeCell]] = cellMatrix): Boolean = {
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
        val res = array.foldLeft("")((current, next) => current + " " + next.toString)
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

  def sameLocation(first: CellInformation, second:CellInformation) = {
      first.location._1 == second.location._1 && first.location._2 == second.location._2
    }

  def forwardAStar(start: (Int, Int), goal: (Int, Int)): SearchResult = {
    @tailrec
    def pathFinder(
      frontier: BinaryHeap[CellInformation],
      sourceMap: mutable.Map[(Int, Int), (Int, Int)],
      costSoFar: mutable.Map[(Int, Int), CostTuple]): SearchResult = {
      if (frontier.isEmpty) {
        return SearchResult(false, sourceMap, costSoFar)
      }
      val current = frontier.dequeue()

      if (current.location equals  goal) {
        return SearchResult(true, sourceMap, costSoFar)
      }
      neibours(current.location, directions).foreach { next =>
        val currentGValue = costSoFar(current.location).gValue
        val newCost = currentGValue + 1
        val oldCost = costSoFar.get(next)
        val newCell = cellMatrix(next._1)(next._2)
        if ((oldCost.isEmpty || newCost < oldCost.get.gValue) && !newCell.blocked) {
          val herrusticValue = herrustic(goal, next)
          val priority = newCost + herrusticValue
          frontier.enqueue(CellInformation(next, priority, newCost))
          costSoFar(next) = CostTuple(newCost, herrusticValue)
          sourceMap(next) = current.location

        }
      }
      pathFinder(frontier, sourceMap, costSoFar)
    }

    val order = MinOrder
    var frontier =  new BinaryHeap[CellInformation](order)
    frontier += CellInformation(start, manhatanDistance(start, goal), 0)
    val sourceMap = new mutable.HashMap[(Int, Int), (Int, Int)]()
    var costSoFar = new mutable.HashMap[(Int, Int), CostTuple]()
    costSoFar += start -> CostTuple(0, herrustic(start, goal))
    pathFinder(frontier, sourceMap, costSoFar)
  }

  def backwardAStar(start: (Int, Int), goal: (Int, Int)) = {
      forwardAStar(goal, start)
  }

  def adaptiveAStar(upperBound: Int)(start: (Int, Int), goal:(Int, Int)): SearchResult ={
    def pathFinder(
      frontier: BinaryHeap[CellInformation],
      sourceMap: mutable.Map[(Int, Int), (Int, Int)],
      costSoFar: mutable.Map[(Int, Int), CostTuple]): (SearchResult, (Int, Int)) = {
      var limit = upperBound
      while (frontier.nonEmpty && limit > 0) {
        val current = frontier.dequeue()
        if (current.location.equals(goal)) {
          return (SearchResult(true, sourceMap, costSoFar), goal)
        }
        neibours(current.location, directions).foreach { next =>
          val currentFValue = costSoFar(current.location).gValue
          val newCost = currentFValue + 1
          val oldCost = costSoFar.get(next)
          val newCell = cellMatrix(next._1)(next._2)
          if ((oldCost.isEmpty || newCost < oldCost.get.gValue) && !newCell.blocked) {
            val hValue = if (oldCost.isEmpty) herrustic(goal, next) else oldCost.get.hValue
            val fValue = newCost + hValue
            costSoFar(next) = CostTuple(newCost, hValue)
            val cellInfo = new CellInformation(next, fValue, newCost)
            frontier.enqueueOrUpdate(cellInfo, sameLocation)
            val sourceOfCurrent = sourceMap.get(current.location)
            if (sourceOfCurrent.isEmpty || sourceOfCurrent.get != next) {
              sourceMap(next) = current.location
            }
            limit -= 1
            print(next + "\t" + newCost + "\t" + hValue + "\t" + limit + "\t")
            if (limit == 0 || next.equals(goal))
              return (SearchResult(true, sourceMap, costSoFar), next)
          }
        }
      }
       (SearchResult(false, sourceMap, costSoFar), goal)
  }
    def repeatedFindPath(start: (Int, Int),
      frontier: BinaryHeap[CellInformation],
      sourceMap: mutable.Map[(Int, Int), (Int, Int)],
      costSoFar: mutable.Map[(Int, Int), CostTuple]): (SearchResult, (Int, Int)) = {
      val (result, endPoint) = pathFinder(frontier, sourceMap, costSoFar)
      println()
      if (!result.success || tupleEqual(endPoint, goal)) {
          return (result, endPoint)
      }

      val (newStart, path) = getPathAndEndPoint(start, endPoint, result.sourceMap)
      val costOfEnd = result.costMap(endPoint)
      path.foreach { point =>
          val current = result.costMap(point)
          current.hValue = costOfEnd.gValue + costOfEnd.hValue - current.gValue
      }
      frontier.removeAll()
      val newCostTuple = result.costMap(newStart)
      newCostTuple.gValue = 0
      frontier += CellInformation(newStart, newCostTuple.hValue, newCostTuple.gValue)
      repeatedFindPath(newStart, frontier, sourceMap, costSoFar)
    }
    val order = MinOrder
    var frontier =  new BinaryHeap[CellInformation](order)
    frontier += CellInformation(start, manhatanDistance(start, goal), 0)
    val sourceMap = new mutable.HashMap[(Int, Int), (Int, Int)]()
    var costSoFar = new mutable.HashMap[(Int, Int), CostTuple]()
    costSoFar += start -> CostTuple(0, manhatanDistance(start, goal))
    val (res, _) = repeatedFindPath(start, frontier, sourceMap, costSoFar)
    res
  }

  def getPathAndEndPoint(startPoint: (Int, Int),
    endPoint: (Int, Int),
    sourceMap: mutable.Map[(Int, Int), (Int, Int)]) = {
    val path = getResultPath(startPoint, endPoint, sourceMap)
    var res = endPoint
    breakable{
      for (index <- path.indices) {
        if (index < path.length-1 && blcokedCell(path(index + 1))) {
          res = path(index)
          break
        }
      }
    }
    (res, path)
  }

  def getResultPath(startPoint:(Int, Int), endPoint: (Int, Int), sourceMap: mutable.Map[(Int, Int), (Int, Int)]) = {
    def mapToList(
      currentPoint: (Int, Int),
      sourceMap: mutable.Map[(Int, Int), (Int, Int)],
      resultList: List[(Int, Int)]): List[(Int, Int)] = {
      val ancestorPoint = sourceMap.get(currentPoint)
      if (ancestorPoint.isEmpty || tupleEqual(startPoint, currentPoint)) {
        return resultList
      }
      mapToList(ancestorPoint.get, sourceMap, ancestorPoint.get :: resultList)
    }
    mapToList(endPoint, sourceMap, List[(Int, Int)](endPoint))
  }

  def tupleEqual(first: (Int, Int), second: (Int, Int)) = first._1 == second._1 && first._2 == second._2
}


object MinOrder extends Ordering[CellInformation] {
  def compare(x:CellInformation, y:CellInformation) = {
    var result = y.fScore compare x.fScore
    if (result == 0) {
      result = y.gScore compare x.gScore
    }
    result
  }
}

case class CostTuple(var gValue: Int, var hValue: Int)

case class CellInformation(location: (Int, Int), fScore: Int, gScore: Int)

case class SearchResult(
  success: Boolean,
  sourceMap: mutable.Map[(Int, Int), (Int, Int)],
  costMap: mutable.Map[(Int, Int), CostTuple]
)
