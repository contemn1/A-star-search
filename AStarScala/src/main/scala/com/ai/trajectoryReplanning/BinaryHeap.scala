package com.ai.trajectoryReplanning

/**
  * Created by zxj on 2017/2/25.
  */
import scala.annotation.tailrec
import scala.collection.mutable.ArrayBuffer

class BinaryHeap[T](val ord: Ordering[T]) {

  private val list = ArrayBuffer.empty[T]
  //private val size = list.size

  def enqueue (element: T): Unit = {
    if (list.isEmpty){
      list  +=  element
    }

    else {
      list += element
      val childIndex = list.size - 1
      bubbleUp(childIndex,parentIndex(childIndex))
    }

  }

  def findIndex(input: T, condition: (T, T) => Boolean): Option[Int] = {
    def findCertain(current: Int, input: T, condition: (T, T) => Boolean): Option[Int] = {
      if (current > list.size - 1) {
        return None
      }
      val currentItem = list(current)
      if (condition(currentItem, input)) {
        return Some(current)
      }
      val left = findCertain(leftChild(current), input, condition)
      if (left.nonEmpty){
        return left
      }
      findCertain(rightChild(current), input, condition)
    }
    if (list.isEmpty) {
      return None
    }
    findCertain(0, input, condition)
  }

  def += (element: T): Unit = enqueue(element)

  private def parentIndex(childIndex: Int) = childIndex /2 + childIndex % 2 - 1

  def enqueueOrUpdate(input: T, condition:(T, T) => Boolean): Unit = {
    val index = findIndex(input, condition).getOrElse(-1)
    if (index < 0){
      enqueue(input)
    }
    else {
      var element = list(index)
      element = input
      listUp(index)
    }
  }

  def removeAll() = list.clear()

  private def bubbleUp[T](indexChild: Int, indexParent: Int) : Unit = {
    if (ord.gt(list(indexChild), list(indexParent))) {
      swap(indexChild, indexParent)
      if(indexParent > 0)
        bubbleUp(indexParent, parentIndex(indexParent))
    }
  }

  def listUp[T](index: Int): Unit ={
    if (index > 0)
      bubbleUp(index, parentIndex(index))
  }

  def getWithIndex(index: Int) = {
    list(index)
  }

  private def swap(index1: Int, index2: Int): Unit = {
    val valueOfIndex1 = list(index1)
    list(index1) = list(index2)
    list(index2) = valueOfIndex1
  }

  def isEmpty(): Boolean = list.isEmpty

  def nonEmpty(): Boolean = list.nonEmpty

  def top(): T = {
    if(list.nonEmpty)
      list.head
    else throw new NullPointerException
  }

  def dequeue(): T = {
    if(list.nonEmpty){
      val elementToReturn = list.head
      swap(0, list.size -1)
      list.remove(list.size - 1)
      bubbleDown(0)
      return elementToReturn
    }
    else throw new NullPointerException
  }

  private def leftChild(index: Int): Int = index * 2 + 1

  private def rightChild(index: Int) = index * 2 + 2

  private def hasLeftChild(index: Int) = leftChild(index) <= list.size - 1

  private def hasRightChild(index :Int) = rightChild(index) <= list.size - 1

  private def nonChild(index: Int) = !hasLeftChild(index)

  @tailrec
  private def bubbleDown(current: Int): Unit = {
      if (nonChild(current)) {
        return
      }
      val left = leftChild(index = current)
      val right = if (hasRightChild(current)) rightChild(current) else left
      val child = if (ord.gt(list(left), list(right))) left else right
      if (!ord.gt(list(current), list(child))) {
        swap(current, child)
        bubbleDown(child)
      }
  }
  def outPut() = list.foreach(println)
}
