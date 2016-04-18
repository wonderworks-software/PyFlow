Function.prototype.bind = function() {
    var func = this;
    var thisObject = arguments[0];
    var args = Array.prototype.slice.call(arguments, 1);
    return function() {
        return func.apply(thisObject, args);
    }
}

//! [0]
function Calculator(ui)
{
    this.ui = ui;

    this.pendingAdditiveOperator = Calculator.NO_OPERATOR;
    this.pendingMultiplicativeOperator = Calculator.NO_OPERATOR;
    this.sumInMemory = 0;
    this.sumSoFar = 0;
    this.factorSoFar = 0;
    this.waitingForOperand = true;

    with (ui) {
        display.text = "0";

        zeroButton.clicked.connect(this.digitClicked.bind(this, 0));
        oneButton.clicked.connect(this.digitClicked.bind(this, 1));
        twoButton.clicked.connect(this.digitClicked.bind(this, 2));
        threeButton.clicked.connect(this.digitClicked.bind(this, 3));
        fourButton.clicked.connect(this.digitClicked.bind(this, 4));
        fiveButton.clicked.connect(this.digitClicked.bind(this, 5));
        sixButton.clicked.connect(this.digitClicked.bind(this, 6));
        sevenButton.clicked.connect(this.digitClicked.bind(this, 7));
        eightButton.clicked.connect(this.digitClicked.bind(this, 8));
        nineButton.clicked.connect(this.digitClicked.bind(this, 9));

        pointButton.clicked.connect(this, "pointClicked");
        changeSignButton.clicked.connect(this, "changeSignClicked");

        backspaceButton.clicked.connect(this, "backspaceClicked");
        clearButton.clicked.connect(this, "clear");
        clearAllButton.clicked.connect(this, "clearAll");

        clearMemoryButton.clicked.connect(this, "clearMemory");
        readMemoryButton.clicked.connect(this, "readMemory");
        setMemoryButton.clicked.connect(this, "setMemory");
        addToMemoryButton.clicked.connect(this, "addToMemory");
  
        divisionButton.clicked.connect(this.multiplicativeOperatorClicked.bind(this, Calculator.DIVISION_OPERATOR));
        timesButton.clicked.connect(this.multiplicativeOperatorClicked.bind(this, Calculator.TIMES_OPERATOR));
        minusButton.clicked.connect(this.additiveOperatorClicked.bind(this, Calculator.MINUS_OPERATOR));
        plusButton.clicked.connect(this.additiveOperatorClicked.bind(this, Calculator.PLUS_OPERATOR));

        squareRootButton.clicked.connect(this.unaryOperatorClicked.bind(this, Calculator.SQUARE_OPERATOR));
        powerButton.clicked.connect(this.unaryOperatorClicked.bind(this, Calculator.POWER_OPERATOR));
        reciprocalButton.clicked.connect(this.unaryOperatorClicked.bind(this, Calculator.RECIPROCAL_OPERATOR));
        equalButton.clicked.connect(this, "equalClicked");
    }
}
//! [0]

Calculator.NO_OPERATOR = 0;
Calculator.SQUARE_OPERATOR = 1;
Calculator.POWER_OPERATOR = 2;
Calculator.RECIPROCAL_OPERATOR = 3;
Calculator.DIVISION_OPERATOR = 4;
Calculator.TIMES_OPERATOR = 5;
Calculator.MINUS_OPERATOR = 6;
Calculator.PLUS_OPERATOR = 7;

Calculator.prototype.abortOperation = function()
{
    this.clearAll();
    this.ui.display.text = "####";
}

Calculator.prototype.calculate = function(rightOperand, pendingOperator)
{
    if (pendingOperator == Calculator.PLUS_OPERATOR) {
        this.sumSoFar += rightOperand;
    } else if (pendingOperator == Calculator.MINUS_OPERATOR) {
        this.sumSoFar -= rightOperand;
    } else if (pendingOperator == Calculator.TIMES_OPERATOR) {
        this.factorSoFar *= rightOperand;
    } else if (pendingOperator == Calculator.DIVISION_OPERATOR) {
        if (rightOperand == 0)
            return false;
        this.factorSoFar /= rightOperand;
    }
    return true;
}

//! [1]
Calculator.prototype.digitClicked = function(digitValue)
{
    if ((digitValue == 0) && (this.ui.display.text == "0"))
        return;
    if (this.waitingForOperand) {
        this.ui.display.clear();
        this.waitingForOperand = false;
    }
    this.ui.display.text += digitValue;
}
//! [1]

Calculator.prototype.unaryOperatorClicked = function(op)
{
    var operand = this.ui.display.text - 0;
    var result = 0;
    if (op == Calculator.SQUARE_OPERATOR) {
        if (operand < 0) {
            this.abortOperation();
            return;
        }
        result = Math.sqrt(operand);
    } else if (op == Calculator.POWER_OPERATOR) {
        result = Math.pow(operand, 2);
    } else if (op == Calculator.RECIPROCAL_OPERATOR) {
        if (operand == 0.0) {
            this.abortOperation();
            return;
        }
        result = 1 / operand;
    }
    this.ui.display.text = result + "";
    this.waitingForOperand = true;
}

Calculator.prototype.additiveOperatorClicked = function(op)
{
    var operand = this.ui.display.text - 0;

    if (this.pendingMultiplicativeOperator != Calculator.NO_OPERATOR) {
        if (!this.calculate(operand, this.pendingMultiplicativeOperator)) {
            this.abortOperation();
            return;
        }
        this.ui.display.text = this.factorSoFar + "";
        operand = this.factorSoFar;
        this.factorSoFar = 0;
        this.pendingMultiplicativeOperator = Calculator.NO_OPERATOR;
    }

    if (this.pendingAdditiveOperator != Calculator.NO_OPERATOR) {
        if (!this.calculate(operand, this.pendingAdditiveOperator)) {
            this.abortOperation();
            return;
        }
        this.ui.display.text = this.sumSoFar + "";
    } else {
        this.sumSoFar = operand;
    }

    this.pendingAdditiveOperator = op;
    this.waitingForOperand = true;
}

Calculator.prototype.multiplicativeOperatorClicked = function(op)
{
    var operand = this.ui.display.text - 0;

    if (this.pendingMultiplicativeOperator != Calculator.NO_OPERATOR) {
        if (!this.calculate(operand, this.pendingMultiplicativeOperator)) {
            this.abortOperation();
            return;
        }
        this.ui.display.text = this.factorSoFar + "";
    } else {
        this.factorSoFar = operand;
    }

    this.pendingMultiplicativeOperator = op;
    this.waitingForOperand = true;
}

Calculator.prototype.equalClicked = function()
{
    var operand = this.ui.display.text - 0;

    if (this.pendingMultiplicativeOperator != Calculator.NO_OPERATOR) {
        if (!this.calculate(operand, this.pendingMultiplicativeOperator)) {
            this.abortOperation();
            return;
        }
        operand = this.factorSoFar;
        this.factorSoFar = 0.0;
        this.pendingMultiplicativeOperator = Calculator.NO_OPERATOR;
    }
    if (this.pendingAdditiveOperator != Calculator.NO_OPERATOR) {
        if (!this.calculate(operand, this.pendingAdditiveOperator)) {
            this.abortOperation();
            return;
        }
        this.pendingAdditiveOperator = Calculator.NO_OPERATOR;
    } else {
        this.sumSoFar = operand;
    }

    this.ui.display.text = this.sumSoFar + "";
    this.sumSoFar = 0.0;
    this.waitingForOperand = true;
}

Calculator.prototype.pointClicked = function()
{
    if (this.waitingForOperand)
        this.ui.display.text = "0";
    if (this.ui.display.text.indexOf(".") == -1)
        this.ui.display.text += ".";
    this.waitingForOperand = false;
}

//! [2]
Calculator.prototype.changeSignClicked = function()
{
    var text = this.ui.display.text;
    var value = text - 0;

    if (value > 0) {
        text = "-" + text;
    } else if (value < 0) {
        text = text.slice(1);
    }
    this.ui.display.text = text;
}
//! [2]

Calculator.prototype.backspaceClicked = function()
{
    if (this.waitingForOperand)
        return;

    var text = this.ui.display.text;
    text = text.slice(0, -1);
    if (text.length == 0) {
        text = "0";
        this.waitingForOperand = true;
    }
    this.ui.display.text = text;
}

Calculator.prototype.clear = function()
{
    if (this.waitingForOperand)
        return;

    this.ui.display.text = "0";
    this.waitingForOperand = true;
}

Calculator.prototype.clearAll = function()
{
    this.sumSoFar = 0.0;
    this.factorSoFar = 0.0;
    this.pendingAdditiveOperator = Calculator.NO_OPERATOR;
    this.pendingMultiplicativeOperator = Calculator.NO_OPERATOR;
    this.ui.display.text = "0";
    this.waitingForOperand = true;
}

Calculator.prototype.clearMemory = function()
{
    this.sumInMemory = 0.0;
}

Calculator.prototype.readMemory = function()
{
    this.ui.display.text = this.sumInMemory + "";
    this.waitingForOperand = true;
}

Calculator.prototype.setMemory = function()
{
    this.equalClicked();
    this.sumInMemory = this.ui.display.text - 0;
}

Calculator.prototype.addToMemory = function()
{
    this.equalClicked();
    this.sumInMemory += this.ui.display.text - 0;
}
