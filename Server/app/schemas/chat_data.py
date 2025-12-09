from pydantic import BaseModel, Field
from typing import Union, Literal, Optional


class ChatRequest(BaseModel):
    message: str


class MarkdownBlock(BaseModel):
    type: Literal["markdown"] = "markdown"
    content: str = Field(..., description="마크다운 형식 텍스트")


class ChartData(BaseModel):
    labels: list[str] = Field(..., description="라벨 배열")
    values: list[float] = Field(..., description="값 배열")


class ChartBlock(BaseModel):
    type: Literal["chart"] = "chart"
    chartType: Literal["bar", "line", "doughnut", "pie", "radar"] = Field(..., description="차트 유형")
    title: str = Field(..., description="차트 제목")
    data: ChartData
    description: Optional[str] = Field(None, description="차트 설명")


class TableBlock(BaseModel):
    type: Literal["table"] = "table"
    title: str = Field(..., description="표 제목")
    headers: list[str] = Field(..., description="열 헤더")
    rows: list[list[str]] = Field(..., description="행 데이터")


class ImageBlock(BaseModel):
    type: Literal["image"] = "image"
    url: str = Field(..., description="이미지 URL")
    alt: str = Field(..., description="대체 텍스트")
    caption: Optional[str] = Field(None, description="캡션")


Block = Union[MarkdownBlock, ChartBlock, TableBlock, ImageBlock]


class ChatResponse(BaseModel):
    blocks: list[Block] = Field(..., description="응답 블록 배열")
