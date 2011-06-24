using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace AI4_AE1
{
    class BDTree
    {
        private int count = 0;
        private BDNode root;
        private BDNode previous;

        private BDNode insert(Point coord, BDNode tree, int level, double accuracy)
        {
            // Create a new node
            if (tree == null)
            {
                BDNode n = new BDNode(coord);
                tree = n;
                if (previous != null)
                    previous.Next = n;
                n.Previous = previous;
                previous = n;
            }
            // the node already exists
            else if (coord.Distance(tree.Coord) <= accuracy)
            {
                if (tree.Previous != null && previous.Coord.Distance(tree.Coord) > tree.Previous.Coord.Distance(tree.Coord))
                {
                    tree.Previous.Next = null;
                    tree.Previous = previous;
                    previous.Next = tree;
                }
                previous = tree;
            }
            // insert on the right
            else if ((level % 2 == 0 && coord.X > tree.Coord.X) || (level % 2 == 1 && coord.Y > tree.Coord.Y))
            {
                tree.Right = insert(coord, tree.Right, level + 1, accuracy);
            }
            // insert on the left
            else
            {
                tree.Left = insert(coord, tree.Left, level + 1, accuracy);
            }

            return tree;
        }

        public Point CurrentPosition(double distance, double angle)
        {
            Point p;
            if (previous == null)
            {
                p = new Point(distance, 0);
            }
            else
            {
                // Touched a wall
                Segment s = new Segment();
                s.Start = previous.Coord;
                s.End = s.Start;
                s.End.X += distance;
                p = new Point(s.Rotate(angle).End);
            }

            return p;
        }

        public void Insert(double distance, double angle, double accuracy)
        {
            Point p = CurrentPosition(distance, angle);

            root = insert(p, root, 0, accuracy);
            count++;
        }

        private static void nearest(BDNode tree, Point target, Rect rect, double max_dist_sqd, int level, NearestNeighborList nnl)
        {
            if (tree == null)
                return;

            Point pivot = tree.Coord;
            double pivot_to_target = pivot.SquareDistance(target);
            Rect left_rect = rect;
            Rect right_rect = new Rect(rect);

            bool target_in_left;
            if (level % 2 == 0)
            {
                left_rect.max.X = pivot.X;
                right_rect.min.X = pivot.X;
                target_in_left = target.X < pivot.X;
            }
            else
            {
                left_rect.max.Y = pivot.Y;
                right_rect.min.Y = pivot.Y;
                target_in_left = target.Y < pivot.Y;
            }

            BDNode nearer_node, further_node;
            Rect nearer_rect, further_rect;
            if (target_in_left)
            {
                nearer_node = tree.Left;
                nearer_rect = left_rect;
                further_node = tree.Right;
                further_rect = right_rect;
            }
            else
            {
                nearer_node = tree.Right;
                nearer_rect = right_rect;
                further_node = tree.Left;
                further_rect = left_rect;
            }

            nearest(nearer_node, target, nearer_rect, max_dist_sqd, level + 1, nnl);

            BDNode nearest_node = (BDNode)nnl.getHighest();
            double dist_sqd;

            if (!nnl.isCapacityReached())
                dist_sqd = Double.MaxValue;
            else
                dist_sqd = nnl.getMaxPriority();

            max_dist_sqd = Math.Min(max_dist_sqd, dist_sqd);

            Point closest = further_rect.Closest(target);
            if (closest.Distance(target) < Math.Sqrt(max_dist_sqd))
            {
                if (pivot_to_target < dist_sqd)
                {
                    nearest_node = tree;

                    dist_sqd = pivot_to_target;

                    nnl.insert(tree, dist_sqd);

                    if (nnl.isCapacityReached())
                        max_dist_sqd = nnl.getMaxPriority();
                    else
                        max_dist_sqd = Double.MaxValue;
                }

                nearest(further_node, target, further_rect, max_dist_sqd, level + 1, nnl);
                BDNode temp_nearest = (BDNode)nnl.getHighest();
                double temp_dist_sqd = nnl.getMaxPriority();

                if (temp_dist_sqd < dist_sqd)
                {
                    nearest_node = temp_nearest;
                    dist_sqd = temp_dist_sqd;
                }
            }
            else if (pivot_to_target < max_dist_sqd)
            {
                nearest_node = tree;
                dist_sqd = pivot_to_target;
            }
        }

        public BDNode[] Nearest(Point p, int n)
        {
            BDNode[] nbrs = new BDNode[n];
            NearestNeighborList nnl = new NearestNeighborList(n);

            Rect rect = Rect.inifiniteRect();
            double max_dist_sqd = Double.MaxValue;
            Point keyp = new Point(p);

            nearest(root, p, rect, max_dist_sqd, 0, nnl);

            for (int i = 0; i < n; ++i)
            {
                BDNode kd = (BDNode)nnl.removeHighest();
                nbrs[n - i - 1] = kd;
            }

            return nbrs;
        }

        private void inorder(BDNode node, List<BDNode> list)
        {
            if (node.Left != null)
                inorder(node.Left, list);
            list.Add(node);
            if (node.Right != null)
                inorder(node.Right, list);
        }

        public List<BDNode> Nodes
        {
            get
            {
                List<BDNode> nodes = new List<BDNode>();
                if (root != null)
                    inorder(root, nodes);
                return nodes;
            }
        }

        public void Path(double distance, double angle, Point target)
        {
            BDNode near = Nearest(CurrentPosition(distance, angle), 1)[0];

        }
    }

    class BDNode
    {
        private Point coord;
        private BDNode prev, next;
        private BDNode left, right;

        public BDNode(Point coord)
        {
            this.coord = coord;
        }

        public Point Coord
        {
            get { return coord; }
        }

        public BDNode Previous
        {
            get { return prev; }
            set { prev = value; }
        }

        public BDNode Next
        {
            get { return next; }
            set { next = value; }
        }

        public BDNode Left
        {
            get { return left; }
            set { left = value; }
        }

        public BDNode Right
        {
            get { return right; }
            set { right = value; }
        }
    }

    public class Rect
    {
        public Point min;
        public Point max;

        public Rect(Rect r)
        {
            this.min = new Point(r.min);
            this.max = new Point(r.max);
        }

        public Rect(Point min, Point max)
        {
            this.min = new Point(min);
            this.max = new Point(max);
        }

        public Point Closest(Point t)
        {
            Point p = new Point();

            if (t.X <= min.X)
                p.X = min.X;
            else if (t.X >= max.X)
                p.X = max.X;
            else
                p.X = t.X;

            if (t.Y <= min.Y)
                p.Y = min.Y;
            else if (t.X >= max.X)
                p.Y = max.Y;
            else
                p.Y = t.Y;

            return p;
        }

        public static Rect inifiniteRect()
        {
            Point min = new Point();
            Point max = new Point();

            min.X = Double.NegativeInfinity;
            min.Y = Double.NegativeInfinity;
            max.X = Double.PositiveInfinity;
            max.Y = Double.PositiveInfinity;

            return new Rect(min, max);
        }
    }

    class PriorityQueue
    {
        /**
         * The maximum priority possible in this priority queue.
         */
        private double maxPriority = Double.MaxValue;

        /**
         * This contains the list of objects in the queue.
         */
        private Object[] data;

        /**
         * This contains the list of prioritys in the queue.
         */
        private double[] value;

        /**
         * Holds the number of elements currently in the queue.
         */
        private int count;

        /**
         * This holds the number elements this queue can have.
         */
        private int capacity;

        /**
         * Creates a new <code>PriorityQueue</code> object. The
         * <code>PriorityQueue</code> object allows objects to be
         * entered into the queue and to leave in the order of
         * priority i.e the highest priority get's to leave first.
         */
        public PriorityQueue()
        {
            init(20);
        }

        /**
         * Creates a new <code>PriorityQueue</code> object. The
         * <code>PriorityQueue</code> object allows objects to
         * be entered into the queue an to leave in the order of
         * priority i.e the highest priority get's to leave first.
         *
         * @param capacity the initial capacity of the queue before
         * a resize
         */
        public PriorityQueue(int capacity)
        {
            init(capacity);
        }

        /**
         * Creates a new <code>PriorityQueue</code> object. The
         * <code>PriorityQueue</code> object allows objects to
         * be entered into the queue an to leave in the order of
         * priority i.e the highest priority get's to leave first.
         *
         * @param capacity the initial capacity of the queue before
         * a resize
         * @param maxPriority is the maximum possible priority for
         * an object
         */
        public PriorityQueue(int capacity, double maxPriority)
        {
            this.maxPriority = maxPriority;
            init(capacity);
        }

        /**
         * This is an initializer for the object. It basically initializes
         * an array of long called value to represent the prioritys of
         * the objects, it also creates an array of objects to be used
         * in parallel with the array of longs, to represent the objects
         * entered, these can be used to sequence the data.
         *
         * @param size the initial capacity of the queue, it can be
         * resized
         */
        private void init(int size)
        {
            capacity = size;
            data = new Object[capacity + 1];
            value = new double[capacity + 1];
            value[0] = maxPriority;
            data[0] = null;
        }

        /**
         * This function adds the given object into the <code>PriorityQueue</code>,
         * its priority is the long priority. The way in which priority can be
         * associated with the elements of the queue is by keeping the priority
         * and the elements array entrys parallel.
         *
         * @param element is the object that is to be entered into this
         * <code>PriorityQueue</code>
         * @param priority this is the priority that the object holds in the
         * <code>PriorityQueue</code>
         */
        public void add(Object element, double priority)
        {
            if (count++ >= capacity)
            {
                expandCapacity();
            }
            /* put this as the last element */
            value[count] = priority;
            data[count] = element;
            bubbleUp(count);
        }

        /**
         * Remove is a function to remove the element in the queue with the
         * maximum priority. Once the element is removed then it can never be
         * recovered from the queue with further calls. The lowest priority
         * object will leave last.
         *
         * @return the object with the highest priority or if it's empty
         * null
         */
        public Object remove()
        {
            if (count == 0)
                return null;
            Object element = data[1];
            /* swap the last element into the first */
            data[1] = data[count];
            value[1] = value[count];
            /* let the GC clean up */
            data[count] = null;
            value[count] = 0L;
            count--;
            bubbleDown(1);
            return element;
        }

        public Object front()
        {
            return data[1];
        }

        public double getMaxPriority()
        {
            return value[1];
        }

        /**
         * Bubble down is used to put the element at subscript 'pos' into
         * it's rightful place in the heap (i.e heap is another name
         * for <code>PriorityQueue</code>). If the priority of an element
         * at subscript 'pos' is less than it's children then it must
         * be put under one of these children, i.e the ones with the
         * maximum priority must come first.
         *
         * @param pos is the position within the arrays of the element
         * and priority
         */
        private void bubbleDown(int pos)
        {
            Object element = data[pos];
            double priority = value[pos];
            int child;
            /* hole is position '1' */
            for (; pos * 2 <= count; pos = child)
            {
                child = pos * 2;
                /* if 'child' equals 'count' then there
                   is only one leaf for this parent */
                if (child != count)

                    /* left_child > right_child */
                    if (value[child] < value[child + 1])
                        child++; /* choose the biggest child */
                /* percolate down the data at 'pos', one level
                   i.e biggest child becomes the parent */
                if (priority < value[child])
                {
                    value[pos] = value[child];
                    data[pos] = data[child];
                }
                else
                {
                    break;
                }
            }
            value[pos] = priority;
            data[pos] = element;
        }

        /**
         * Bubble up is used to place an element relatively low in the
         * queue to it's rightful place higher in the queue, but only
         * if it's priority allows it to do so, similar to bubbleDown
         * only in the other direction this swaps out its parents.
         *
         * @param pos the position in the arrays of the object
         * to be bubbled up
         */
        private void bubbleUp(int pos)
        {
            Object element = data[pos];
            double priority = value[pos];
            /* when the parent is not less than the child, end*/
            while (value[pos / 2] < priority)
            {
                /* overwrite the child with the parent */
                value[pos] = value[pos / 2];
                data[pos] = data[pos / 2];
                pos /= 2;
            }
            value[pos] = priority;
            data[pos] = element;
        }

        /**
         * This ensures that there is enough space to keep adding elements
         * to the priority queue. It is however advised to make the capacity
         * of the queue large enough so that this will not be used as it is
         * an expensive method. This will copy across from 0 as 'off' equals
         * 0 is contains some important data.
         */
        private void expandCapacity()
        {
            capacity = count * 2;
            Object[] elements = new Object[capacity + 1];
            double[] prioritys = new double[capacity + 1];
            Array.Copy(data, 0, elements, 0, data.Length);
            Array.Copy(value, 0, prioritys, 0, data.Length);
            data = elements;
            value = prioritys;
        }

        /**
         * This method will empty the queue. This also helps garbage
         * collection by releasing any reference it has to the elements
         * in the queue. This starts from offset 1 as off equals 0
         * for the elements array.
         */
        public void clear()
        {
            for (int i = 1; i < count; i++)
            {
                data[i] = null; /* help gc */
            }
            count = 0;
        }

        /**
         * The number of elements in the queue. The length
         * indicates the number of elements that are currently
         * in the queue.
         *
         * @return the number of elements in the queue
         */
        public int length()
        {
            return count;
        }
    }

    public class NearestNeighborList
    {
        public static int REMOVE_HIGHEST = 1;
        public static int REMOVE_LOWEST = 2;

        PriorityQueue m_Queue = null;
        int m_Capacity = 0;

        // constructor
        public NearestNeighborList(int capacity)
        {
            m_Capacity = capacity;
            m_Queue = new PriorityQueue(m_Capacity, Double.PositiveInfinity);
        }

        public double getMaxPriority()
        {
            if (m_Queue.length() == 0)
            {
                return Double.PositiveInfinity;
            }
            return m_Queue.getMaxPriority();
        }

        public bool insert(Object _object, double priority)
        {
            if (m_Queue.length() < m_Capacity)
            {
                // capacity not reached
                m_Queue.add(_object, priority);
                return true;
            }
            if (priority > m_Queue.getMaxPriority())
            {
                // do not insert - all elements in queue have lower priority
                return false;
            }
            // remove object with highest priority
            m_Queue.remove();
            // add new object
            m_Queue.add(_object, priority);
            return true;
        }

        public bool isCapacityReached()
        {
            return m_Queue.length() >= m_Capacity;
        }

        public Object getHighest()
        {
            return m_Queue.front();
        }

        public bool isEmpty()
        {
            return m_Queue.length() == 0;
        }

        public int getSize()
        {
            return m_Queue.length();
        }

        public Object removeHighest()
        {
            // remove object with highest priority
            return m_Queue.remove();
        }

    }
}
