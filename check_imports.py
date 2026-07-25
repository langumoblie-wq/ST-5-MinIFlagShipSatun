with open('src/App.tsx', 'r') as f:
    content = f.read()

if 'Printer' not in content:
    content = content.replace('PieChart, TrendingUp, AlertCircle, Network, BookOpen,', 'PieChart, TrendingUp, AlertCircle, Network, BookOpen, Printer,')
    with open('src/App.tsx', 'w') as f:
        f.write(content)
    print("Added Printer to imports")
else:
    print("Printer already imported")
