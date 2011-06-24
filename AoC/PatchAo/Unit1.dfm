object Form1: TForm1
  Left = 0
  Top = 0
  Caption = 'Age of Conan Diffie-Hellman key modifier'
  ClientHeight = 142
  ClientWidth = 498
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 13
  object Label1: TLabel
    Left = 12
    Top = 19
    Width = 38
    Height = 13
    Caption = 'Offset :'
  end
  object Label2: TLabel
    Left = 8
    Top = 40
    Width = 125
    Height = 13
    Caption = 'Current Key in the Client :'
  end
  object Label3: TLabel
    Left = 8
    Top = 86
    Width = 67
    Height = 13
    Caption = 'Key to inject :'
  end
  object Edit1: TEdit
    Left = 53
    Top = 16
    Width = 73
    Height = 21
    TabOrder = 0
    Text = '011CBAD0'
  end
  object Edit2: TEdit
    Left = 8
    Top = 55
    Width = 401
    Height = 21
    TabOrder = 1
  end
  object Edit3: TEdit
    Left = 8
    Top = 102
    Width = 401
    Height = 21
    TabOrder = 2
  end
  object Button1: TButton
    Left = 417
    Top = 55
    Width = 73
    Height = 21
    Caption = 'Read'
    TabOrder = 3
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 417
    Top = 102
    Width = 73
    Height = 21
    Caption = 'Write'
    TabOrder = 4
    OnClick = Button2Click
  end
end
