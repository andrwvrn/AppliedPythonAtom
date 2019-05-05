#!/usr/bin/env python
# coding: utf-8
import numpy as np


class NotFittedError(Exception):

    def __init__(self):
        message = "Data is not fitted yet. Call 'fit' method before using this method."
        Exception.__init__(self, message)


class Splitter:

    def compute_impurity(self, y):
        '''
        Метод считает коэффициент Джини для множества y
        '''
        classes = np.unique(y)
        n_samples = y.shape[0]
        prob = np.array([])

        if len(classes) <= 1:
            impurity = 0
            return impurity

        for cls in classes:
            prob = np.append(prob, ((np.sum(y == cls) / n_samples)**2))
        impurity = 1 - np.sum(prob)

        return impurity

    def compute_split_information(self, X, y, th):
        '''
        Вспомогательный метод, позволяющий посчитать прирост информации для заданного разбиения
        :param X: Матрица (num_objects, 1) - срез по какой-то 1 фиче, по которой считаем разбиение
        :param y: Матрица (num_object, 1) - целевые переменные
        :param th: Порог, который проверяется
        :return: прирост информации
        '''
        left_child_ = y[X <= th]
        right_child_ = y[X > th]

        n_samples = y.shape[0]
        n_samples_left = left_child_.shape[0]
        n_samples_right = right_child_.shape[0]

        gini_before_split = self.compute_impurity(y)
        gini_left = self.compute_impurity(left_child_)
        gini_right = self.compute_impurity(right_child_)

        inf_gain = gini_before_split - (n_samples_left / n_samples) * gini_left -\
            (n_samples_right / n_samples) * gini_right
        return inf_gain

    def make_split(self, X, y, feat_num, threshold):
        '''
        Метод разбивает матрицы X и y по признаку с номером feat_num
        в зависимости от значения threshold
        '''
        left_child_X = X[X[:, feat_num] <= threshold]
        left_child_y = y[X[:, feat_num] <= threshold]

        right_child_X = X[X[:, feat_num] > threshold]
        right_child_y = y[X[:, feat_num] > threshold]

        return left_child_X, left_child_y, right_child_X, right_child_y


class RegularTreeBuilder:

    def __init__(self, max_depth, min_leaf_size, min_inform_criter):
        '''
        Метод инициализирует атрибуты, в которых будет храниться информация о дереве
        '''
        self._max_depth = max_depth
        self._min_leaf_size = min_leaf_size
        self._min_inform_criter = min_inform_criter

        self._feature = np.array([]).astype(int)
        self._threshold = np.array([])
        self._pred = np.array([])
        self._left_child_id = np.array([]).astype(int)
        self._right_child_id = np.array([]).astype(int)
        self._depth = 0
        self._node_count = 0
        self._splitter = Splitter()

    def _build_tree(self, X_train, y_train, node_id=0):
        '''
        Метод рекурсивно строит дерево
        '''
        inf_gain = np.zeros(X_train.shape)

        self._pred = np.append(self._pred, np.bincount(y_train).argmax())  # append prediction for current node

        for i in range(X_train.shape[1]):
            for j in range(X_train.shape[0]):
                inf_gain[:, i][j] = self._splitter.compute_split_information(X_train[:, i], y_train,
                                                                             X_train[:, i][j])

        split_idx = np.unravel_index(np.argmax(inf_gain), inf_gain.shape)
        feat_num = split_idx[1]
        threshold = X_train[split_idx]

        node_id = self._node_count

        if self.check_criteria(X_train, inf_gain[split_idx], split_idx):
            self._depth += 1

            self._feature = np.append(self._feature, feat_num)      # append splitting feature number
            self._threshold = np.append(self._threshold, threshold)  # append splitting feature

            left_child_X, left_child_y, right_child_X, right_child_y = self._splitter.make_split(X_train,
                                                                                                 y_train,
                                                                                                 feat_num,
                                                                                                 threshold)

            self._node_count += 1
            self._left_child_id = np.append(self._left_child_id, self._node_count)
            self._right_child_id = np.append(self._right_child_id, -3)

            self._build_tree(left_child_X, left_child_y, node_id)

            self._node_count += 1
            self._right_child_id[node_id] = self._node_count

            self._build_tree(right_child_X, right_child_y, node_id)

            self._depth -= 1                        # decrease depth to process nodes on previous level
        else:
            self._left_child_id = np.append(self._left_child_id, -1)
            self._right_child_id = np.append(self._right_child_id, -1)
            self._feature = np.append(self._feature, -2)
            self._threshold = np.append(self._threshold, -2)

    def check_criteria(self, X, inf_gain, split_idx):
        '''
        Метод проверяет параметры дерева на соответствие переданным при инициализации
        '''
        if self._max_depth is not None and self._depth >= self._max_depth:
            return False
        elif inf_gain <= self._min_inform_criter:
            return False
        elif np.sum(X[:, split_idx[1]] <= X[split_idx]) < self._min_leaf_size or\
                np.sum(X[:, split_idx[1]] > X[split_idx]) < self._min_leaf_size:
            return False
        else:
            return True


class BestFirstTreeBuilder:

    def __init__(self, max_depth, min_leaf_size, max_leaf_number, min_inform_criter):
        '''
        Метод инициализирует атрибуты, в которых будет храниться информация о дереве
        '''
        self._max_depth = max_depth
        self._min_leaf_size = min_leaf_size
        self._max_leaf_number = max_leaf_number
        self._min_inform_criter = min_inform_criter

        self._feature = np.array([]).astype(int)
        self._threshold = np.array([])
        self._pred = np.array([])
        self._left_child_id = np.array([]).astype(int)
        self._right_child_id = np.array([]).astype(int)

        self._node_count = 0
        self._node_list = []
        self._leaves_count = 1
        self._splitter = Splitter()

    class Node:

        def __init__(self, node_id=-1, X=-1, y=-1, pred=-1, inf_gain=-1,
                     split_idx=-1, feat_num=-2, threshold=-2, depth=-1,
                     left_child_id=-1, right_child_id=-1):
            self._node_id = node_id
            self._X_elements = X
            self._y_elements = y
            self._pred = pred
            self._inf_gain = inf_gain
            self._split_idx = split_idx
            self._feat_num = feat_num
            self._threshold = threshold
            self._node_depth = depth
            self._left_child_id = left_child_id
            self._right_child_id = right_child_id

    def _set_tree(self, X, y):
        '''
        Метод инициализирует корень дерева и, начиная с него, запускает построение дерева
        '''
        root_node = self._set_node(X, y, depth=0)
        self._node_list.append(root_node)
        if self.check_criteria(root_node._X_elements, root_node._inf_gain,
                               root_node._split_idx, root_node):
            self._build_best_first_tree(current_node=root_node)

    def _set_node(self, X_train, y_train, depth):
        '''
        Метод создает узлы дерева и считает для каждого узла значения атрибутов
        '''
        inf_gain = np.zeros(X_train.shape)

        for i in range(X_train.shape[1]):
            for j in range(X_train.shape[0]):
                inf_gain[:, i][j] = self._splitter.compute_split_information(X_train[:, i], y_train,
                                                                             X_train[:, i][j])

        split_idx = np.unravel_index(np.argmax(inf_gain), inf_gain.shape)
        best_inf_gain = inf_gain[split_idx]
        feat_num = split_idx[1]
        threshold = X_train[split_idx]
        pred = np.bincount(y_train).argmax()

        return self.Node(node_id=self._node_count, X=X_train, y=y_train, pred=pred, inf_gain=best_inf_gain,
                         split_idx=split_idx, feat_num=feat_num, depth=depth, threshold=threshold)

    def _build_best_first_tree(self, current_node):
        '''
        Метод строит дерево, выбирая лучшие листы
        '''
        leaf_nodes = []
        self._leaves_count += 1
        left_child_X, left_child_y, right_child_X, right_child_y = self._splitter.make_split(
                                                                                   current_node._X_elements,
                                                                                   current_node._y_elements,
                                                                                   current_node._feat_num,
                                                                                   current_node._threshold)
        self._node_count += 1
        current_node._left_child_id = self._node_count
        left_child_node = self._set_node(left_child_X, left_child_y, depth=current_node._node_depth+1)

        self._node_count += 1
        current_node._right_child_id = self._node_count
        right_child_node = self._set_node(right_child_X, right_child_y, depth=current_node._node_depth+1)

        self._node_list.append(left_child_node)
        self._node_list.append(right_child_node)

        self._node_list.sort(key=lambda x: x._inf_gain, reverse=True)
        next_node = None

        for node in self._node_list:
            if node._left_child_id == node._right_child_id and self.check_criteria(node._X_elements,
                                                                                   node._inf_gain,
                                                                                   node._split_idx, node):
                next_node = node

        if next_node is not None:
            self._build_best_first_tree(next_node)
        else:
            self._node_list.sort(key=lambda x: x._node_id)
            self._prepare_pred(self._node_list[0])

    def _prepare_pred(self, node):
        '''
        Метод располагает узлы дерева и их атрибуты для рекурсивного прохода по ним
        при вызове метода predict
        '''
        self._feature = np.append(self._feature, node._feat_num)
        self._threshold = np.append(self._threshold, node._threshold)
        self._pred = np.append(self._pred, node._pred)
        self._left_child_id = np.append(self._left_child_id, node._left_child_id)
        self._right_child_id = np.append(self._right_child_id, node._right_child_id)
        if node._left_child_id != node._right_child_id:
            self._prepare_pred(self._node_list[node._left_child_id])
            self._prepare_pred(self._node_list[node._right_child_id])

    def check_criteria(self, X, inf_gain, split_idx, node):
        '''
        Метод проверяет параметры дерева на соответствие параметрам, переданным в методе __init__
        класса DecisionTreeClassifier
        '''
        if self._max_depth is not None and node._node_depth >= self._max_depth:
                return False
        elif self._leaves_count >= self._max_leaf_number:
                return False
        elif inf_gain <= self._min_inform_criter:
            return False
        elif np.sum(X[:, split_idx[1]] <= X[split_idx]) < self._min_leaf_size or\
                np.sum(X[:, split_idx[1]] > X[split_idx]) < self._min_leaf_size:
            return False
        return True


class DecisionTreeClassifier:
    '''
    Пишем свой велосипед - дерево для классификации
    '''
    def __init__(self, max_depth=None, min_leaf_size=1, max_leaf_number=None, min_inform_criter=0.0):
        '''
        Инициализируем наше дерево
        :param max_depth: один из возможных критерием останова - максимальная глубина дерева
        :param min_leaf_size: один из возможных критериев останова - число элементов в листе
        :param max_leaf_number: один из возможных критериев останова - число листов в дереве.
        Нужно подумать как нам отобрать "лучшие" листы
        :param min_inform_criter: один из критериев останова - процент прироста информации, который
        считаем незначительным
        '''
        self._max_depth = max_depth
        self._min_leaf_size = min_leaf_size
        self._max_leaf_number = max_leaf_number
        self._min_inform_criter = min_inform_criter

    def fit(self, X, y):
        '''
        Стендартный метод обучения
        :param X: матрица объекто-признаков (num_objects, num_features)
        :param y: матрица целевой переменной (num_objects, 1)
        :return: None
        '''
        if (X.shape[0] != y.shape[0]):
            raise ValueError(f"Found input variables with inconsistent numbers of"
                             f" samples: {X.shape[0]} != {len(y)}.")

        self.check_parameters(self._max_depth, self._min_leaf_size, self._max_leaf_number,
                              self._min_inform_criter)

        self._n_features = X.shape[1]

        if self._max_leaf_number is None:
            self.tree_ = RegularTreeBuilder(self._max_depth, self._min_leaf_size,
                                            self._min_inform_criter)
            self.tree_._build_tree(X, y)
        else:
            self.tree_ = BestFirstTreeBuilder(self._max_depth, self._min_leaf_size, self._max_leaf_number,
                                              self._min_inform_criter)
            self.tree_._set_tree(X, y)

    def predict(self, X):
        '''
        Метод для предсказания меток на объектах X
        :param X: матрица объектов-признаков (num_objects, num_features)
        :return: вектор предсказаний (num_objects, 1)
        '''
        if getattr(self, 'tree_', None) is None:
            raise NotFittedError
        elif self._n_features != X.shape[1]:
            raise ValueError(f"Number of features of the model must match the input. "
                             f"Model n_features is {self._n_features} and input n_features is {X.shape[1]}.")
        self._counter = -1
        idx = np.arange(X.shape[0]).astype(int)
        self._idx_pred = []
        self._get_prediction(X, idx)
        pred = np.zeros(X.shape[0]).astype(int)
        for idx_pred in self._idx_pred:
            if len(idx_pred[0]) == 0:
                continue
            else:
                pred[idx_pred[0]] = idx_pred[1]
        return pred

    def predict_proba(self, X):
        '''
        Метод, возвращающий предсказания принадлежности к классу
        :param X: матрица объектов-признаков (num_objects, num_features)
        :return: вектор предсказанных вероятностей (num_objects, num_classes)
        '''
        if getattr(self, 'tree_', None) is None:
            raise NotFittedError
        elif self._n_features != X.shape[1]:
            raise ValueError(f"Number of features of the model must match the input. "
                             f"Model n_features is {self._n_features} and input n_features is {X.shape[1]}.")
        pred = self.predict(X)
        proba = np.zeros((X.shape[0], np.max(pred)+1))
        for (i, cls) in enumerate(pred):
            proba[i][cls] = 1
        return proba

    def _get_prediction(self, X, idx):
        '''
        Метод разбивает матрицу признаков и матрицу индексов предсказаний
        в соответствии с построенным деревом. Для каждого разбиения мы будем
        знать индексы строк детей справа и слева и предсказания для них.
        '''
        self._counter += 1

        if self.tree_._left_child_id[self._counter] == self.tree_._right_child_id[self._counter]:
            self._idx_pred.append([idx, self.tree_._pred[self._counter]])
        else:
            feat_num = self.tree_._feature[self._counter]
            threshold = self.tree_._threshold[self._counter]

            l_child_X, l_child_pred_idx, r_child_X, r_child_pred_idx = self.tree_._splitter.make_split(X, idx,
                                                                                                       feat_num,
                                                                                                       threshold)
            self._get_prediction(l_child_X, l_child_pred_idx)
            self._get_prediction(r_child_X, r_child_pred_idx)

    def check_parameters(self, max_depth, min_leaf_size, max_leaf_number, min_inform_criter):
        '''
        Метод проверяет на валидность параметры дерева
        '''
        if max_depth is not None and max_depth < 0:
            raise ValueError("Parameter max_depth must be greater than zero.")
        elif min_leaf_size < 1:
            raise ValueError("Parameter min_leaf_size must be greater than or equal to 1.")
        elif max_leaf_number is not None and max_leaf_number <= 1:
            raise ValueError(f"Parameter max_leaf_number {max_leaf_number} must be "
                             f"either None or larger than 1.")
        elif min_inform_criter < 0:
            raise ValueError("Parameter min_inform_criter must be greater than or equal to 0.")
