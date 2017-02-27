package com.ai.trajectoryReplanning

import javafx.application.Application
import javafx.beans.property.{SimpleIntegerProperty, SimpleStringProperty}
import javafx.collections.FXCollections
import javafx.geometry.{Insets, Orientation}
import javafx.scene.control._
import javafx.scene.layout.{HBox, StackPane, TilePane, VBox}
import javafx.scene.paint.Color
import javafx.scene.shape.Rectangle
import javafx.stage.Stage
import javafx.scene.{Group, Scene}

import scalafx.util.converter.NumberStringConverter
/**
  * Created by zxj on 2017/2/25.
  */
class Demo extends Application{
    val sceneWidth = 1200.0
    val sceneHeight = 800.0
    val playField = Array.ofDim[Mynode](101, 101)
    val scrollPane = new ScrollPane()
    val textFieldStartX = createTextField(0)
    val textFieldStartY = createTextField(0)
    val textFieldEndX = createTextField(100)
    val textFieldEndY = createTextField(100)
    val startX = new SimpleIntegerProperty(0)
    val startY = new SimpleIntegerProperty(0)
    val endX = new SimpleIntegerProperty(100)
    val endY = new SimpleIntegerProperty(100)
    var pathList = List[(Int, Int)]()
    var closeList = List[(Int, Int)]()
    var reversed = false
    val mazeGeneratorTest = MazeGeneratorTest
    val firstMatrix = mazeGeneratorTest.initCellMatrix(101)
    val generator = new MazeGenerator(firstMatrix)
    generator.generateBlcoks()
    val algorithms: Array[((Int, Int), (Int, Int)) => SearchResult] =
      Array(generator.forwardAStar, generator.forwardAStar, generator.adaptiveAStar(8))
    var algorithm: ((Int, Int), (Int, Int)) => SearchResult = generator.forwardAStar
  override def start (primaryStage: Stage) = {

     val root = new Group()
     val gridWidth = 10.0
     val gridHeight = 10.0
     for (i <- generator.cellMatrix.indices;
          j <- generator.cellMatrix(i).indices) {
       val node = new Mynode(i * gridWidth, j * gridHeight, gridWidth, gridHeight, generator.isWall((i, j)))
        node.init()
        root.getChildren.add(node)
        playField(i)(j) = node
     }
     scrollPane.setPrefSize(800, 800)
     scrollPane.setContent(root)
    textBinding(textFieldStartX, startX)
    textBinding(textFieldStartY, startY)
    textBinding(textFieldEndX, endX)
    textBinding(textFieldEndY, endY)
    val vbox = addVBox()
    val pathButton = findPathButton()
    val cancelButton = new Button("cancel")
    cancelButton.setOnAction {(_) =>
      setColor(closeList, Color.WHITE)

    }

    val actionBox = new HBox()
    actionBox.getChildren.addAll(pathButton, cancelButton)
    vbox.getChildren.addAll(
      addTilePan("StartX", "StartY", textFieldStartX, textFieldStartY),
      addTilePan("EndX", "EndY", textFieldEndX, textFieldEndY),
      algorithmChoiceBox(),
      actionBox
    )
     val hBox = addHBox(scrollPane, vbox)
     val scene = new Scene(hBox, sceneWidth, sceneHeight)
     primaryStage.setScene(scene)
     primaryStage.show()
   }

  def addHBox(scrollPane: ScrollPane, vBox: VBox) = {
    val hbox = new HBox()
    hbox.setPadding(new Insets(15, 12, 15, 12))
    hbox.setSpacing(10)
    hbox.getChildren.addAll(scrollPane, vBox)
    hbox
  }

  def addVBox() = {
    val vbox = new VBox()
    vbox.setPadding(new Insets(10))
    vbox.setSpacing(20)
    vbox
  }

  def algorithmChoiceBox() = {
    val cb = new ChoiceBox(FXCollections.observableArrayList("Forward AStar", "Backword AStar", "Adaptive AStar"))
    cb.getSelectionModel.selectedIndexProperty().addListener { (_, _, newValue) =>
      algorithm = algorithms(newValue.intValue())
      reversed = newValue.intValue() == 1
    }
    cb.getSelectionModel.selectFirst()
    cb
  }

  def findPathButton() = {
    val button = new Button("find path")
    button.setOnAction{(_) =>
      setColor(closeList, Color.WHITE)
      setColor(pathList, Color.WHITE)
      val start = (startX.intValue(), startY.intValue())
      val end = (endX.intValue(), endY.intValue())
      val result = if (!reversed) algorithm(start, end) else algorithm(end, start)
      val succeed = result.success
      val resultMap = result.sourceMap
      if (succeed) {
        val finalNode = if (reversed) start else end
        val resultList = mazeGeneratorTest.getResultPath(finalNode, resultMap)
        pathList = resultList
        closeList = result.costMap.keys.toList
        setColor(result.costMap.keys, Color.PINK)
        setColor(resultList, Color.RED)
        println(closeList.size)
        println(pathList.size)
      }
      playField(startX.intValue())(startY.intValue()).setFillColor(Color.BLUE)
      playField(endX.intValue())(endY.intValue()).setFillColor(Color.GREEN)
    }
    button
  }

  def setColor(list: Iterable[(Int, Int)], color: Color): Unit = {
    list.foreach { tuple =>
      val (x, y) = tuple
      val current = playField(x)(y)
      if (current.unBlocked()) {
        current.setFillColor(color)
      }
    }
  }

  def addTilePan(firstLabel: String, secondLabel: String, textFieldX: TextField, textFieldY: TextField) = {
    val tilePane = new TilePane(Orientation.HORIZONTAL)
    tilePane.setPadding(new Insets(0, 0, 0, 0))
    tilePane.setHgap(10)
    val labelX = new Label(firstLabel)
    val labelY = new Label(secondLabel)
    tilePane.getChildren.addAll(labelX, textFieldX, labelY, textFieldY)
    tilePane
  }

  def createTextField(initial: Int) = {
    val textField = new TextField()
    textField.setPrefWidth(50)
    textField
  }

  def textBinding(textField: TextField, value: SimpleIntegerProperty): Unit = {
      textField.textProperty().bindBidirectional(value, new NumberStringConverter())
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
  def setFillColor(color: Color) = rectangle.setFill(color)
  def unBlocked() = !blocked
}