package com.ai.trajectoryReplanning

import javafx.application.Application
import javafx.scene.layout.StackPane
import javafx.scene.paint.Color
import javafx.scene.shape.Rectangle
import javafx.stage.Stage
import javafx.scene.{Group, Scene}
/**
  * Created by zxj on 2017/2/25.
  */
class Demo extends Application{
    val sceneWidth = 888.0
    val sceneHeight = 888.0
    val playField = Array.ofDim[Mynode](101, 101)
   override def start (primaryStage: Stage) = {
    val mazeGeneratorTest = MazeGeneratorTest
     val firstMatrix = mazeGeneratorTest.initCellMatrix(101)
     val generator = new MazeGenerator(firstMatrix)
      generator.generateBlcoks()

     val root = new Group()
     val gridWidth = 8.0
     val gridHeight = 8.0
     for (i <- 0 to generator.cellMatrix.length -1;
          j <- 0 to generator.cellMatrix(i).length -1) {
       val node = new Mynode(i * gridWidth, j * gridHeight, gridWidth, gridHeight, generator.isWall((i, j)))
        node.init()
        root.getChildren.add(node)
       if (i == 20 && j == 30) {
         node.rectangle.setFill(Color.RED)
       }
       if (i == 80 && j == 90) {
         node.rectangle.setFill(Color.BLUE)
       }
        playField(i)(j) = node
     }

     val scene = new Scene(root, sceneWidth, sceneHeight)
     primaryStage.setScene(scene)
     primaryStage.show()
   }
}

object Demo {
  def main (args: Array[String]): Unit = {
    Application.launch(classOf[Demo], args:_*)
  }
}

class Mynode(x: Double, y:Double, width: Double, height: Double, blocked: Boolean) extends StackPane {
  val rectangle = new Rectangle(width, height)
  def init() = {
    rectangle.setStroke(Color.BLACK)
    val fill = if (blocked) Color.BLACK else Color.WHITE
    rectangle.setFill(fill)
    setTranslateX(x)
    setTranslateY(y)
    getChildren.addAll(rectangle)
  }
}