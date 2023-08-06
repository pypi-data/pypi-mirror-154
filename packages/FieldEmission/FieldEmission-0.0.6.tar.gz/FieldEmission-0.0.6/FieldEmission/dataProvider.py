import re
from statistics import mean
import numpy as np
from enum import Flag, auto


class ClipFlags(Flag):
    Below = auto()
    Above = auto()
    Equal = auto()
    BelowAndAbove = Below | Above


class SplitFlags(Flag):
    OverlapInLoRows = auto()
    OverlapInHiRows = auto()
    OverlapInBothRows = OverlapInLoRows | OverlapInHiRows


class DataProvider:
    def __init__(self, ColumnHeader, NumpyArray: np.ndarray):
        if type(ColumnHeader) == dict:
            self.ColumnHeader = ColumnHeader
        else:
            ColCnt = len(ColumnHeader)
            self.ColumnHeader = {ColumnHeader[i]: range(ColCnt)[i] for i in range(ColCnt)}
        if not type(NumpyArray) == np.ndarray:
            self.Data = np.array(NumpyArray).transpose()
        else:
            self.Data = NumpyArray

        self.__DetermineColumns__()
        if not self.Columns == len(ColumnHeader):
            raise ValueError("ColumnHeader-count not matching with DataColumns-count.")
        self.__DetermineRows__()

    def ClipData(self, iColumn: int, ValueExcluded, ClipFlag: ClipFlags):
        clipCol = self.GetColumn(iColumn)
        removeIndicies = []
        for iRow in range(len(clipCol)):
            if ClipFlags.Above in ClipFlag and clipCol[iRow] > ValueExcluded:
                removeIndicies.append(iRow)
            if ClipFlags.Below in ClipFlag and clipCol[iRow] < ValueExcluded:
                removeIndicies.append(iRow)
            if ClipFlags.Equal in ClipFlag and clipCol[iRow] == ValueExcluded:
                removeIndicies.append(iRow)

        self.RemoveRows(removeIndicies)
        return
    


    def GetData(self):
        return self.Data

    def GetRow(self, RowIndex):
        return self.Data[RowIndex, :]
    
    def SetRow(self, RowIndex, RowValues):
        self.Data[RowIndex, :] = RowValues

    def RemoveRows(self, RowIndicies):
        self.Data = np.delete(self.Data, RowIndicies, axis=0)
        self.__DetermineRows__()
        return
    
    def KeepRows(self, RowIndicies):
        if not type(RowIndicies) == range:
            RowIndicies = range(RowIndicies[0], RowIndicies[1])

        self.Data = self.Data[RowIndicies, :]
        self.__DetermineRows__()
    
    def MultiplyColumn(self, Column, Scalar):
        self.Data[:, self.__GetColumnIndexFromKey__(Column)] = np.multiply(self.Data[:, self.__GetColumnIndexFromKey__(Column)] , Scalar)
        return

    def DivideColumn(self, Column, Scalar):
        self.Data[:, self.__GetColumnIndexFromKey__(Column)] = np.divide(self.Data[:, self.__GetColumnIndexFromKey__(Column)], Scalar)
        return

    def DivideByColumn(self, Column, Scalar):
        self.Data[:, self.__GetColumnIndexFromKey__(Column)] = np.divide(Scalar, self.Data[:, self.__GetColumnIndexFromKey__(Column)])
        return

    def AddToColumn(self, Column, Scalar):
        self.Data[:, self.__GetColumnIndexFromKey__(Column)] = np.add(self.Data[:, self.__GetColumnIndexFromKey__(Column)],Scalar)
        return

    def SubtractFromColumn(self, Column, Scalar):
        self.Data[:, self.__GetColumnIndexFromKey__(Column)] = np.subtract(self.Data[:, self.__GetColumnIndexFromKey__(Column)], Scalar)
        return

    def SubtractColumnFrom(self, Column, Scalar):
        self.Data[:, self.__GetColumnIndexFromKey__(Column)] = np.subtract(Scalar, self.Data[:, self.__GetColumnIndexFromKey__(Column)])
        return

    def SplitDataAtRow(self, Index: int, SplitFlag: SplitFlags = SplitFlags.OverlapInBothRows):
        cRows = self.Rows
        Index = int(Index)
        # The short ifs define where the overlapping index is stored (loRows, hiRows or both!)
        loRows = self.Data[0 : Index + (1 if SplitFlags.OverlapInLoRows in SplitFlag else 0)]
        hiRows = self.Data[Index + (0 if SplitFlags.OverlapInHiRows in SplitFlag else 1) : cRows]

        return loRows, np.flip(hiRows, axis=0)
    
    def SeparateLineRepeats(self, RepeatsPerLine):
        # Check if Rows is a multiple of RepeatsPerLine!
        if not (self.Rows % RepeatsPerLine) == 0:
            raise "Error: Datarows not a multiple of given RepeatsPerLine."

        # Preparation
        tarRows = int(self.Rows / RepeatsPerLine)
        headerCells = [None] * self.Columns
        dataCells = [None] * self.Columns

        # Data manupulation
        for col in range(self.Columns):
            newData = np.reshape(self.GetColumn(col), (tarRows, RepeatsPerLine))
            newMean = np.zeros((tarRows, 1))
            for i in range(tarRows):
                newMean[i] = mean(newData[i, :])

            dataHeader = [None] * (RepeatsPerLine + 1) # Single Points + 1xMean
            currHeadName = self.__GetKeyFromColumnIndex__(col)
            for i in range(RepeatsPerLine):
                dataHeader[i] = currHeadName + "-Pnt" + str(i)
            dataHeader[i + 1] = currHeadName + "-Mean"

            headerCells[col] = dataHeader
            dataCells[col] = np.column_stack((newData, newMean))

        # Create new combined data
        header = [None]
        dataShape = np.shape(dataCells[0])
        dataMatrix = np.zeros((dataShape[0], 1))
        for col in range(self.Columns):
            header = np.append(header, headerCells[col])
            dataMatrix = np.column_stack((dataMatrix, dataCells[col]))
            
        header = np.delete(header, 0).tolist() # Remove [None] column and convert back to list
        dataMatrix = np.delete(dataMatrix, 0, axis=1) # Remove [None] column
        dataBuilder = DataProvider(header, dataMatrix)

        # Use another DataProvider to build the new data and grab it from there
        self.ColumnHeader = dataBuilder.ColumnHeader
        self.Data = dataBuilder.Data
        self.__DetermineColumns__()
        self.__DetermineRows__()
        return

    def __RemoveRowsFromNumpyarray__(nparray: np.ndarray, Indicies):
        return np.delete(nparray, Indicies, axis=0)

    def __DetermineRows__(self):
        self.Rows = np.size(self.Data, axis=0)

    def __DetermineColumns__(self):
        self.Columns = np.size(self.Data, axis=1)

    def GetColumn(self, Column):
        return self.Data[:, self.__GetColumnIndexFromKey__(Column)]

    def SetColumn(self, Column, ColumnValues):
        self.Data[:, self.__GetColumnIndexFromKey__(Column)] = ColumnValues
        return

    def AppendColumn(self, Column, ColumnValues):
        if not self.Rows == len(ColumnValues):
            raise "Error: Given column not matching in rows"
            
        self.ColumnHeader[Column] = self.Columns
        self.Data = np.column_stack((self.Data, ColumnValues))
        self.__DetermineColumns__()
        return

    def RemoveColumn(self, ColumnIndicies):
        for columnIndex in ColumnIndicies:
            for key, value in self.ColumnHeader.items():
                if value == columnIndex:
                    self.ColumnHeader.pop(key)
                    break

        self.Data = np.delete(self.Data, ColumnIndicies, axis=1)
        self.__DetermineColumns__()
        return

    def __GetColumnIndexFromKey__(self, Column):
        if type(Column) == str:
            return self.ColumnHeader[Column]
        else:
            return Column

    def __GetKeyFromColumnIndex__(self, ColumnIndex):
        if type(ColumnIndex) == int:
            for key, value in self.ColumnHeader.items():
                if ColumnIndex ==  value:
                    return key
        else:
            return ColumnIndex